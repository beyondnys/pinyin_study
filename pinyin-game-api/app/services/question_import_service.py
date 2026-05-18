"""练习册题目批量导入服务。"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.practice_book import PracticeBook
from app.models.practice_question import PracticeQuestion
from app.models.word_library import WordLibrary
from app.services.pinyin_service import extract_unique_hanzi, hanzi_to_pinyin
from app.utils.pinyin_util import apply_pinyin_fields


def batch_import_book_questions(
    db: Session,
    book_id: int,
    raw_text: str,
    operator_id: int,
) -> dict:
    """
    从文本批量导入题目到指定练习册。

    - 自动去除非汉字字符
    - 本练习册已有汉字跳过
    - 字库已有汉字不再写入字库（仍会导入到本练习册，若本册尚无该字）
    """
    book = db.query(PracticeBook).filter(PracticeBook.id == book_id, PracticeBook.is_deleted == 0).first()
    if not book:
        raise ValueError("练习册不存在")

    # 统计被过滤的非汉字数量（粗略：原文长度 - 提取后拼接长度）
    hanzi_list = extract_unique_hanzi(raw_text)
    invalid_stripped = max(0, len(raw_text) - len(hanzi_list))

    book_hanzi = {
        q.hanzi
        for q in db.query(PracticeQuestion)
        .filter(PracticeQuestion.book_id == book_id, PracticeQuestion.is_deleted == 0)
        .all()
    }
    lib_hanzi = {
        w.hanzi
        for w in db.query(WordLibrary).filter(WordLibrary.is_deleted == 0).all()
    }

    skipped_in_book: list[str] = []
    skipped_in_library: list[str] = []  # 字库已有、本次未写入字库的字
    to_add: list[str] = []

    for hz in hanzi_list:
        if hz in book_hanzi:
            skipped_in_book.append(hz)
            continue
        to_add.append(hz)

    sort_order = (
        db.query(PracticeQuestion)
        .filter(PracticeQuestion.book_id == book_id, PracticeQuestion.is_deleted == 0)
        .count()
    )
    added_hanzi: list[str] = []

    for hz in to_add:
        py_result = hanzi_to_pinyin(hz)
        q = PracticeQuestion(
            book_id=book_id,
            hanzi=hz,
            pinyin="",
            pinyin_list="[]",
            sort_order=sort_order,
            created_by=operator_id,
            updated_by=operator_id,
        )
        apply_pinyin_fields(q, py_result)
        db.add(q)
        if hz not in lib_hanzi:
            word = WordLibrary(
                hanzi=hz,
                pinyin="",
                pinyin_list="[]",
                pinyin_plain="",
                remark="练习册批量导入",
                created_by=operator_id,
                updated_by=operator_id,
            )
            apply_pinyin_fields(word, py_result)
            db.add(word)
            lib_hanzi.add(hz)
        else:
            skipped_in_library.append(hz)
        book_hanzi.add(hz)
        added_hanzi.append(hz)
        sort_order += 1

    book.question_count = sort_order
    db.commit()

    return {
        "added_count": len(added_hanzi),
        "added_hanzi": added_hanzi,
        "skipped_in_book": skipped_in_book,
        "skipped_in_library": skipped_in_library,
        "invalid_stripped": invalid_stripped,
    }
