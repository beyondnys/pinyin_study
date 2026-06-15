"""词语连连看词库：候选题目提供者。"""

from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from app.learning.types import CandidateItem, ContentRef, ContentType
from app.models.word_question import WordQuestion


def list_book_candidates(db: Session, book_id: int) -> List[CandidateItem]:
    """列出词库下全部未删除题目。"""
    questions = (
        db.query(WordQuestion)
        .filter(WordQuestion.book_id == book_id, WordQuestion.is_deleted == 0)
        .order_by(WordQuestion.sort_order, WordQuestion.id)
        .all()
    )
    return [
        CandidateItem(
            content=ContentRef(ContentType.WORD_CHOICE, q.id),
            question_id=q.id,
            hanzi=q.word,
            pinyin=q.pinyin,
        )
        for q in questions
    ]
