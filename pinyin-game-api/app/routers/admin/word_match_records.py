"""词语连连看学习记录（管理端）。"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.user import User
from app.models.word_book import WordBook
from app.models.word_match_record import WordMatchRecord
from app.response import success

router = APIRouter(dependencies=[Depends(require_admin)])


@router.get("")
def list_word_match_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user_id: Optional[int] = None,
    book_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """分页查询词语连连看学习记录。"""
    q = db.query(WordMatchRecord).filter(WordMatchRecord.is_deleted == 0)
    if user_id:
        q = q.filter(WordMatchRecord.user_id == user_id)
    if book_id:
        q = q.filter(WordMatchRecord.book_id == book_id)
    total = q.count()
    records = (
        q.order_by(WordMatchRecord.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    items = []
    for r in records:
        user = db.query(User).filter(User.id == r.user_id).first()
        book = db.query(WordBook).filter(WordBook.id == r.book_id).first()
        items.append(
            {
                "id": r.id,
                "user_id": r.user_id,
                "username": user.username if user else "",
                "book_id": r.book_id,
                "book_title": book.title if book else "",
                "record_type": "word_match",
                "total_count": r.total_count,
                "correct_count": r.correct_count,
                "accuracy": float(r.accuracy),
                "duration_seconds": r.duration_seconds,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
        )
    return success({"total": total, "items": items})
