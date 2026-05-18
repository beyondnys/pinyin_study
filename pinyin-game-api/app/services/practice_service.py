"""练习与游戏服务。"""

from __future__ import annotations

import random
import uuid
from decimal import Decimal
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from app.models.practice_answer_detail import PracticeAnswerDetail
from app.models.practice_book import PracticeBook
from app.models.practice_question import PracticeQuestion
from app.models.practice_record import PracticeRecord
from app.models.word_library import WordLibrary
from app.learning import LearningMasteryService
from app.schemas.practice import AnswerItem, GameCardOut, GameDataOut
from app.services.wrong_question_service import upsert_wrong_questions
from app.utils.pinyin_util import is_pinyin_match

def get_book_or_404(db: Session, book_id: int) -> PracticeBook:
    """获取启用中的练习册。"""
    book = (
        db.query(PracticeBook)
        .filter(PracticeBook.id == book_id, PracticeBook.is_deleted == 0, PracticeBook.status == 1)
        .first()
    )
    if not book:
        raise ValueError("练习册不存在或已下架")
    return book


def _cards_from_pairs(
    pairs: List[Tuple[int, str, str]],
) -> List[GameCardOut]:
    """由 (question_id, hanzi, pinyin) 列表生成打乱后的卡片。"""
    cards: List[GameCardOut] = []
    for qid, hanzi, pinyin in pairs:
        cards.append(
            GameCardOut(
                card_id=f"h-{qid}-{uuid.uuid4().hex[:6]}",
                question_id=qid,
                card_type="hanzi",
                text=hanzi,
            )
        )
        cards.append(
            GameCardOut(
                card_id=f"p-{qid}-{uuid.uuid4().hex[:6]}",
                question_id=qid,
                card_type="pinyin",
                text=pinyin,
            )
        )
    random.shuffle(cards)
    return cards


def build_game_data(
    db: Session,
    book_id: int,
    pick_count: int = 8,
    user_id: Optional[int] = None,
) -> GameDataOut:
    """
    构建配对游戏：按掌握度加权抽取 pick_count 道题（不足则全用），再打乱卡片。
    未登录或未传 user_id 时退化为均匀随机。
    """
    book = get_book_or_404(db, book_id)

    if user_id:
        mastery = LearningMasteryService(db)
        picked = mastery.pick_pinyin_book_questions(user_id, book_id, pick_count)
        if not picked:
            raise ValueError("该练习册暂无题目，请在后台添加或执行演示数据脚本")
        pairs = [(c.question_id, c.hanzi, c.pinyin) for c in picked]
    else:
        questions = (
            db.query(PracticeQuestion)
            .filter(PracticeQuestion.book_id == book_id, PracticeQuestion.is_deleted == 0)
            .all()
        )
        if not questions:
            raise ValueError("该练习册暂无题目，请在后台添加或执行演示数据脚本")
        if len(questions) > pick_count:
            questions = random.sample(questions, pick_count)
        pairs = [(q.id, q.hanzi, q.pinyin) for q in questions]
    cards = _cards_from_pairs(pairs)
    return GameDataOut(book_id=book.id, book_title=book.title, total=len(pairs), cards=cards)


def _resolve_answer(
    db: Session, book_id: int, ans: AnswerItem
) -> Optional[Tuple[str, str, int, bool]]:
    """
    解析单条答案，返回 (hanzi, correct_pinyin, question_id, is_correct)。
    question_id 为虚拟负 id 时从字库读取。
    """
    if ans.question_id > 0:
        q = (
            db.query(PracticeQuestion)
            .filter(
                PracticeQuestion.id == ans.question_id,
                PracticeQuestion.is_deleted == 0,
            )
            .first()
        )
        if not q:
            return None
        ok = is_pinyin_match(ans.user_pinyin, q.pinyin, q.pinyin_list)
        return q.hanzi, q.pinyin, q.id, ok

    if ans.question_id < 0:
        w = db.query(WordLibrary).filter(WordLibrary.id == -ans.question_id, WordLibrary.is_deleted == 0).first()
        if not w:
            return None
        ok = is_pinyin_match(ans.user_pinyin, w.pinyin, w.pinyin_list)
        return w.hanzi, w.pinyin, ans.question_id, ok
    return None


def submit_practice(
    db: Session,
    user_id: int,
    book_id: int,
    answers: list[AnswerItem],
    duration_seconds: int,
) -> PracticeRecord:
    """提交练习结果，写入记录、明细与错题。"""
    record_book_id = book_id
    if book_id <= 0:
        fallback = (
            db.query(PracticeBook)
            .filter(PracticeBook.is_deleted == 0, PracticeBook.status == 1)
            .order_by(PracticeBook.id)
            .first()
        )
        record_book_id = fallback.id if fallback else 0
    else:
        get_book_or_404(db, book_id)

    correct = 0
    details: list[PracticeAnswerDetail] = []
    wrong_items: list[tuple[str, str, int]] = []

    mastery_svc = LearningMasteryService(db)
    effective_book_id = record_book_id if record_book_id > 0 else book_id

    for ans in answers:
        resolved = _resolve_answer(db, book_id, ans)
        if not resolved:
            continue
        hanzi, correct_pinyin, qid, is_ok = resolved
        if qid > 0 and effective_book_id > 0:
            mastery_svc.record_pinyin_attempt(user_id, effective_book_id, qid, is_ok)
        if is_ok:
            correct += 1
        else:
            wrong_items.append((hanzi, correct_pinyin, record_book_id or 0))
        details.append(
            PracticeAnswerDetail(
                record_id=0,
                question_id=max(qid, 0),
                hanzi=hanzi,
                user_pinyin=ans.user_pinyin,
                correct_pinyin=correct_pinyin,
                is_correct=1 if is_ok else 0,
                created_by=user_id,
                updated_by=user_id,
            )
        )

    total = len(details) or 1
    accuracy = round(correct / total * 100, 2)

    record = PracticeRecord(
        user_id=user_id,
        book_id=record_book_id,
        total_count=total,
        correct_count=correct,
        accuracy=Decimal(str(accuracy)),
        duration_seconds=duration_seconds,
        created_by=user_id,
        updated_by=user_id,
    )
    db.add(record)
    db.flush()

    for d in details:
        d.record_id = record.id
        db.add(d)

    if wrong_items:
        upsert_wrong_questions(db, user_id, wrong_items)

    db.commit()
    db.refresh(record)
    return record
