"""错题查询（管理端）。"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.user import User
from app.models.wrong_question import WrongQuestion
from app.response import success

router = APIRouter(dependencies=[Depends(require_admin)])


@router.get("")
def list_wrong(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """分页错题列表。"""
    q = db.query(WrongQuestion).filter(WrongQuestion.is_deleted == 0)
    if user_id:
        q = q.filter(WrongQuestion.user_id == user_id)
    total = q.count()
    rows = q.order_by(WrongQuestion.last_wrong_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    items = []
    for w in rows:
        user = db.query(User).filter(User.id == w.user_id).first()
        items.append(
            {
                "id": w.id,
                "user_id": w.user_id,
                "username": user.username if user else "",
                "book_id": w.book_id,
                "hanzi": w.hanzi,
                "pinyin": w.pinyin,
                "wrong_count": w.wrong_count,
                "last_wrong_at": w.last_wrong_at.isoformat() if w.last_wrong_at else None,
            }
        )
    return success({"total": total, "items": items})
