"""词语连连看游戏服务。"""

from __future__ import annotations

import random
import uuid
from decimal import Decimal
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from app.learning import LearningMasteryService
from app.models.word_book import WordBook
from app.models.word_match_answer_detail import WordMatchAnswerDetail
from app.models.word_match_record import WordMatchRecord
from app.models.word_question import WordQuestion
from app.schemas.word_match import (
    WordCharCardOut,
    WordMatchAnswerItem,
    WordMatchGameDataOut,
    WordMetaOut,
)
from app.services.pinyin_service import hanzi_to_char_pinyin_list
from app.services.tts.tts_audio_service import get_audio_urls_by_texts, lookup_word_match_audio_map
from app.services.wrong_question_service import upsert_wrong_questions
from app.utils.word_split_util import (
    DEFAULT_PICK_WORDS,
    MAX_PICK_WORDS,
    MAX_TOTAL_CARDS,
    pick_words_for_full_grid,
    split_word_chars,
    validate_word,
)


def get_word_book_or_404(db: Session, book_id: int) -> WordBook:
    """获取启用中的词语词库。"""
    book = (
        db.query(WordBook)
        .filter(WordBook.id == book_id, WordBook.is_deleted == 0, WordBook.status == 1)
        .first()
    )
    if not book:
        raise ValueError("词库不存在或已下架")
    return book


def _cards_from_words(
    db: Session,
    pairs: List[Tuple[int, str, int]],
    audio_map: Optional[dict] = None,
) -> tuple[List[WordMetaOut], List[WordCharCardOut]]:
    """由 (question_id, word, word_len) 生成单字卡片（含逐字拼音与朗读 URL）并打乱。"""
    audio_map = audio_map or {}
    words_meta: List[WordMetaOut] = []
    cards: List[WordCharCardOut] = []

    # 批量查单字 TTS（字库/历史生成过的同字可读）
    all_chars: set[str] = set()
    for _, word, _ in pairs:
        all_chars.update(split_word_chars(word))
    char_audio_map = get_audio_urls_by_texts(db, list(all_chars))

    for qid, word, wlen in pairs:
        words_meta.append(
            WordMetaOut(
                question_id=qid,
                word=word,
                word_len=wlen,
                audio_url=audio_map.get(qid),
            )
        )
        chars = split_word_chars(word)
        char_pinyins = hanzi_to_char_pinyin_list(word)
        for idx, ch in enumerate(chars):
            cards.append(
                WordCharCardOut(
                    card_id=f"c-{qid}-{idx}-{uuid.uuid4().hex[:6]}",
                    question_id=qid,
                    char_index=idx,
                    text=ch,
                    pinyin=char_pinyins[idx] if idx < len(char_pinyins) else "",
                    audio_url=char_audio_map.get(ch),
                )
            )

    random.shuffle(cards)
    return words_meta, cards


def build_word_match_game(
    db: Session,
    book_id: int,
    pick_count: int = DEFAULT_PICK_WORDS,
    user_id: Optional[int] = None,
    max_cards: int = MAX_TOTAL_CARDS,
) -> WordMatchGameDataOut:
    """
    构建词语连连看：加权抽词（默认 6 个），总卡数不超过 max_cards（16）。
    每字一卡，前端按 char_index 顺序连字。
    """
    book = get_word_book_or_404(db, book_id)

    if user_id:
        mastery = LearningMasteryService(db)
        picked = mastery.pick_word_book_questions(user_id, book_id, pick_count, max_cards)
        if not picked:
            raise ValueError("该词库暂无题目，请在后台添加词语")
        pairs = [(c.question_id, c.hanzi, len(c.hanzi)) for c in picked]
    else:
        questions = (
            db.query(WordQuestion)
            .filter(WordQuestion.book_id == book_id, WordQuestion.is_deleted == 0)
            .all()
        )
        if not questions:
            raise ValueError("该词库暂无题目，请在后台添加词语")
        random.shuffle(questions)
        tuples = [(q.id, q.word, q.word_len) for q in questions]
        trimmed = pick_words_for_full_grid(tuples, max_words=MAX_PICK_WORDS)
        pairs = trimmed

    qids = [p[0] for p in pairs]
    audio_map = lookup_word_match_audio_map(db, qids)
    words_meta, cards = _cards_from_words(db, pairs, audio_map)

    return WordMatchGameDataOut(
        book_id=book.id,
        book_title=book.title,
        total=len(pairs),
        total_cards=len(cards),
        words=words_meta,
        cards=cards,
    )


def submit_word_match(
    db: Session,
    user_id: int,
    book_id: int,
    answers: list[WordMatchAnswerItem],
    duration_seconds: int,
) -> WordMatchRecord:
    """提交词语连连看成绩。"""
    get_word_book_or_404(db, book_id)

    correct = 0
    details: list[WordMatchAnswerDetail] = []
    mastery_svc = LearningMasteryService(db)

    for ans in answers:
        q = (
            db.query(WordQuestion)
            .filter(
                WordQuestion.id == ans.question_id,
                WordQuestion.book_id == book_id,
                WordQuestion.is_deleted == 0,
            )
            .first()
        )
        if not q:
            continue
        # 提交时出现在 answers 里的视为连对
        is_ok = True
        correct += 1
        mastery_svc.record_word_attempt(user_id, book_id, q.id, is_ok)
        details.append(
            WordMatchAnswerDetail(
                record_id=0,
                question_id=q.id,
                word=q.word,
                is_correct=1,
                created_by=user_id,
                updated_by=user_id,
            )
        )

    total = len(details) or 1
    accuracy = round(correct / total * 100, 2)

    record = WordMatchRecord(
        user_id=user_id,
        book_id=book_id,
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

    db.commit()
    db.refresh(record)
    return record


def record_word_wrong_attempt(
    db: Session,
    user_id: int,
    book_id: int,
    question_id: int,
) -> bool:
    """
    连字顺序错误时记错题并更新掌握度。
    返回 True 表示已记录。
    """
    q = (
        db.query(WordQuestion)
        .filter(
            WordQuestion.id == question_id,
            WordQuestion.book_id == book_id,
            WordQuestion.is_deleted == 0,
        )
        .first()
    )
    if not q:
        return False

    get_word_book_or_404(db, book_id)
    upsert_wrong_questions(db, user_id, [(q.word, q.pinyin, book_id)])
    LearningMasteryService(db).record_word_attempt(user_id, book_id, question_id, False)
    db.commit()
    return True


def apply_pinyin_to_word_question(q: WordQuestion) -> None:
    """为词语题目填充拼音字段。"""
    from app.services.pinyin_service import hanzi_to_pinyin
    from app.utils.pinyin_util import encode_pinyin_list

    result = hanzi_to_pinyin(q.word)
    q.pinyin = result.pinyin
    q.pinyin_list = result.pinyin_list_json or encode_pinyin_list([result.pinyin])


def _refresh_book_question_count(db: Session, book_id: int) -> None:
    """重算词库题目数量（批量导入时只调用一次）。"""
    book = db.query(WordBook).filter(WordBook.id == book_id).first()
    if not book:
        return
    book.question_count = (
        db.query(WordQuestion)
        .filter(WordQuestion.book_id == book_id, WordQuestion.is_deleted == 0)
        .count()
    )


def create_word_question(
    db: Session,
    book_id: int,
    word: str,
    meaning: str | None = None,
    sort_order: int = 0,
    operator_id: int | None = None,
    *,
    commit: bool = True,
) -> WordQuestion:
    """创建词语题目并更新词库计数。批量导入时可传 commit=False 由外层统一提交。"""
    validated = validate_word(word)
    book = db.query(WordBook).filter(WordBook.id == book_id, WordBook.is_deleted == 0).first()
    if not book:
        raise ValueError("词库不存在")

    q = WordQuestion(
        book_id=book_id,
        word=validated,
        word_len=len(validated),
        meaning=meaning,
        sort_order=sort_order,
        created_by=operator_id,
        updated_by=operator_id,
    )
    apply_pinyin_to_word_question(q)
    db.add(q)
    db.flush()
    _refresh_book_question_count(db, book_id)
    if commit:
        db.commit()
        db.refresh(q)
    return q


def batch_import_word_questions(
    db: Session,
    book_id: int,
    raw_text: str,
    operator_id: int | None = None,
) -> dict:
    """
    批量导入词语到指定词库（单次事务，避免逐条 commit 导致超时）。

    - 每行一个 2～4 字词
    - 本词库已有词语跳过
    - 返回 created_ids 供后台 TTS 任务使用
    """
    book = db.query(WordBook).filter(WordBook.id == book_id, WordBook.is_deleted == 0).first()
    if not book:
        raise ValueError("词库不存在")

    existing_words = {
        q.word
        for q in db.query(WordQuestion)
        .filter(WordQuestion.book_id == book_id, WordQuestion.is_deleted == 0)
        .all()
    }

    lines = [ln.strip() for ln in raw_text.splitlines() if ln.strip()]
    sort_order = len(existing_words)
    created_ids: list[int] = []
    errors: list[str] = []
    skipped: list[str] = []
    seen_in_batch: set[str] = set()

    for i, line in enumerate(lines, 1):
        if line in seen_in_batch:
            continue
        seen_in_batch.add(line)
        try:
            validated = validate_word(line)
        except ValueError as e:
            errors.append(f"第{i}行: {e}")
            continue
        if validated in existing_words:
            skipped.append(validated)
            continue

        q = WordQuestion(
            book_id=book_id,
            word=validated,
            word_len=len(validated),
            sort_order=sort_order,
            created_by=operator_id,
            updated_by=operator_id,
        )
        apply_pinyin_to_word_question(q)
        db.add(q)
        db.flush()
        created_ids.append(q.id)
        existing_words.add(validated)
        sort_order += 1

    if created_ids:
        _refresh_book_question_count(db, book_id)
        db.commit()
    elif errors:
        db.rollback()

    return {
        "created": len(created_ids),
        "created_ids": created_ids,
        "errors": errors,
        "skipped": skipped,
    }
