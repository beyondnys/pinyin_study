"""前台错题本。"""

from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.wrong_question import WrongQuestion
from app.response import success
from app.schemas.wrong import WrongQuestionOut

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("")
def my_wrong_questions(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """当前用户错题列表。"""
    items = (
        db.query(WrongQuestion)
        .filter(WrongQuestion.user_id == user["user_id"], WrongQuestion.is_deleted == 0)
        .order_by(WrongQuestion.last_wrong_at.desc())
        .all()
    )
    return success([WrongQuestionOut.model_validate(w).model_dump() for w in items])
