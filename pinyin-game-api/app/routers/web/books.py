"""前台练习册接口。"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.practice_book import PracticeBook
from app.response import fail, success
from app.schemas.book import BookOut
from app.services.practice_service import build_game_data

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("")
def list_books(db: Session = Depends(get_db)):
    """获取已启用的练习册列表。"""
    items = (
        db.query(PracticeBook)
        .filter(PracticeBook.is_deleted == 0, PracticeBook.status == 1)
        .order_by(PracticeBook.id.desc())
        .all()
    )
    return success([BookOut.model_validate(b).model_dump() for b in items])


@router.get("/{book_id}/game")
def get_game(
    book_id: int,
    count: int = Query(8, ge=4, le=16, description="从练习册加权抽取题目数"),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """获取配对游戏卡片；按掌握度加权抽题（错题优先）并打乱。"""
    try:
        data = build_game_data(db, book_id, pick_count=count, user_id=user["user_id"])
    except ValueError as e:
        return fail(1, str(e))
    return success(data.model_dump())
