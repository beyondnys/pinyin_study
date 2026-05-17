"""学习记录查询（管理端）。"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.practice_book import PracticeBook
from app.models.practice_record import PracticeRecord
from app.models.user import User
from app.response import success

router = APIRouter(dependencies=[Depends(require_admin)])


@router.get("")
def list_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user_id: Optional[int] = None,
    book_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """分页查询学习记录。"""
    q = db.query(PracticeRecord).filter(PracticeRecord.is_deleted == 0)
    if user_id:
        q = q.filter(PracticeRecord.user_id == user_id)
    if book_id:
        q = q.filter(PracticeRecord.book_id == book_id)
    total = q.count()
    records = q.order_by(PracticeRecord.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

    items = []
    for r in records:
        user = db.query(User).filter(User.id == r.user_id).first()
        book = db.query(PracticeBook).filter(PracticeBook.id == r.book_id).first()
        items.append(
            {
                "id": r.id,
                "user_id": r.user_id,
                "username": user.username if user else "",
                "book_id": r.book_id,
                "book_title": book.title if book else "",
                "total_count": r.total_count,
                "correct_count": r.correct_count,
                "accuracy": float(r.accuracy),
                "duration_seconds": r.duration_seconds,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
        )
    return success({"total": total, "items": items})
