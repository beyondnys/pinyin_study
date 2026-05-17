"""拼音练习册：候选题目提供者。"""

from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from app.learning.types import CandidateItem, ContentRef, ContentType
from app.models.practice_question import PracticeQuestion


def list_book_candidates(db: Session, book_id: int) -> List[CandidateItem]:
    """列出练习册下全部未删除题目。"""
    questions = (
        db.query(PracticeQuestion)
        .filter(PracticeQuestion.book_id == book_id, PracticeQuestion.is_deleted == 0)
        .order_by(PracticeQuestion.sort_order, PracticeQuestion.id)
        .all()
    )
    return [
        CandidateItem(
            content=ContentRef(ContentType.PINYIN_PAIR, q.id),
            question_id=q.id,
            hanzi=q.hanzi,
            pinyin=q.pinyin,
        )
        for q in questions
    ]
