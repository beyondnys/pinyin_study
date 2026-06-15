"""自适应学习对外服务：加权抽题 + 记录作答。"""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from app.learning import mastery_engine
from app.learning.providers import pinyin_book_provider, word_book_provider
from app.utils.word_split_util import MAX_PICK_WORDS, MAX_TOTAL_CARDS, pick_words_for_full_grid
from app.learning.repository import MasteryRepository
from app.learning.sampler import weighted_sample_without_replacement
from app.learning.types import (
    CandidateItem,
    ContentRef,
    ContentType,
    LearningScope,
    MasteryState,
    ScopeType,
    WeightedCandidate,
)
from app.utils.datetime_util import utc_now


def book_scope(book_id: int) -> LearningScope:
    """练习册场景。"""
    return LearningScope(ScopeType.BOOK, book_id)


class LearningMasteryService:
    """掌握度模块门面，供 practice_service 调用。"""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = MasteryRepository(db)

    def pick_pinyin_book_questions(
        self,
        user_id: int,
        book_id: int,
        pick_count: int,
    ) -> List[CandidateItem]:
        """
        从练习册按掌握度加权抽取 pick_count 道题。
        错题权重高，未做题中等，已掌握且未到复习日权重低但仍 > 0。
        """
        candidates = pinyin_book_provider.list_book_candidates(self.db, book_id)
        if not candidates:
            return []
        if len(candidates) <= pick_count:
            return candidates

        scope = book_scope(book_id)
        mastery_map = self.repo.get_map(
            user_id,
            scope,
            ContentType.PINYIN_PAIR,
            [c.content.content_id for c in candidates],
        )
        now = utc_now()

        weighted: List[WeightedCandidate] = []
        for c in candidates:
            row = mastery_map.get(c.content.content_id)
            w, state = mastery_engine.compute_sample_weight(row, now)
            weighted.append(WeightedCandidate(item=c, weight=w, state=state))

        picked = weighted_sample_without_replacement(weighted, pick_count)
        return [p.item for p in picked]

    def record_pinyin_attempt(
        self,
        user_id: int,
        book_id: int,
        question_id: int,
        is_correct: bool,
    ) -> None:
        """
        记录单次作答（配对题一题一次判定）。
        每次答错都会累加 wrong_count；答对增加 streak 并按间隔设置 next_review_at。
        """
        if question_id <= 0:
            return

        scope = book_scope(book_id)
        content = ContentRef(ContentType.PINYIN_PAIR, question_id)
        orm_row = self.repo.get_or_create_row(user_id, scope, content, user_id)

        data = mastery_engine.row_from_orm(orm_row)
        if data.state == MasteryState.UNSEEN and orm_row.total_attempts == 0:
            data = mastery_engine.default_row()

        now = utc_now()
        if is_correct:
            data = mastery_engine.apply_correct(data, now)
        else:
            data = mastery_engine.apply_wrong(data, now)

        orm_row.total_attempts += 1
        self.repo.save_row_data(orm_row, data, user_id)

    def pick_word_book_questions(
        self,
        user_id: int,
        book_id: int,
        pick_count: int,
        max_cards: int = MAX_TOTAL_CARDS,
    ) -> List[CandidateItem]:
        """
        从词语词库按掌握度加权抽题，且总卡数不超过 max_cards。
        优先接近 pick_count 个词，超出卡数上限时自动减少词数。
        """
        candidates = word_book_provider.list_book_candidates(self.db, book_id)
        if not candidates:
            return []

        scope = book_scope(book_id)
        mastery_map = self.repo.get_map(
            user_id,
            scope,
            ContentType.WORD_CHOICE,
            [c.content.content_id for c in candidates],
        )
        now = utc_now()

        weighted: List[WeightedCandidate] = []
        for c in candidates:
            row = mastery_map.get(c.content.content_id)
            w, state = mastery_engine.compute_sample_weight(row, now)
            weighted.append(WeightedCandidate(item=c, weight=w, state=state))

        # 扩大加权样本池，再按 16/15 卡优选子集（4 行最多空 1 格）
        pool_n = min(len(weighted), max(pick_count * 4, 16))
        if len(candidates) <= pool_n:
            ordered = candidates
        else:
            picked = weighted_sample_without_replacement(weighted, pool_n)
            ordered = [p.item for p in picked]

        tuples = [(c.question_id, c.hanzi, len(c.hanzi)) for c in ordered]
        trimmed = pick_words_for_full_grid(tuples, max_words=MAX_PICK_WORDS)
        trimmed_ids = [t[0] for t in trimmed]
        by_id = {c.question_id: c for c in ordered}
        return [by_id[qid] for qid in trimmed_ids if qid in by_id]

    def record_word_attempt(
        self,
        user_id: int,
        book_id: int,
        question_id: int,
        is_correct: bool,
    ) -> None:
        """记录词语连连看单次判定（连对/连错）。"""
        if question_id <= 0:
            return

        scope = book_scope(book_id)
        content = ContentRef(ContentType.WORD_CHOICE, question_id)
        orm_row = self.repo.get_or_create_row(user_id, scope, content, user_id)

        data = mastery_engine.row_from_orm(orm_row)
        if data.state == MasteryState.UNSEEN and orm_row.total_attempts == 0:
            data = mastery_engine.default_row()

        now = utc_now()
        if is_correct:
            data = mastery_engine.apply_correct(data, now)
        else:
            data = mastery_engine.apply_wrong(data, now)

        orm_row.total_attempts += 1
        self.repo.save_row_data(orm_row, data, user_id)
