"""前台词语词库接口。"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.word_book import WordBook
from app.response import fail, success
from app.schemas.word_match import WordBookOut
from app.services.word_match_service import build_word_match_game
from app.utils.word_split_util import DEFAULT_PICK_WORDS, MAX_PICK_WORDS, MAX_TOTAL_CARDS

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("")
def list_word_books(db: Session = Depends(get_db)):
    """获取已启用的词语词库列表。"""
    items = (
        db.query(WordBook)
        .filter(WordBook.is_deleted == 0, WordBook.status == 1)
        .order_by(WordBook.id.desc())
        .all()
    )
    return success([WordBookOut.model_validate(b).model_dump() for b in items])


@router.get("/{book_id}/game")
def get_word_match_game(
    book_id: int,
    count: int = Query(DEFAULT_PICK_WORDS, ge=3, le=MAX_PICK_WORDS, description="抽取词语数上限，总卡数优先 16/15"),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """获取词语连连看单字卡片；按掌握度加权抽词并打乱。"""
    try:
        data = build_word_match_game(
            db,
            book_id,
            pick_count=count,
            user_id=user["user_id"],
            max_cards=MAX_TOTAL_CARDS,
        )
    except ValueError as e:
        return fail(1, str(e))
    return success(data.model_dump())
