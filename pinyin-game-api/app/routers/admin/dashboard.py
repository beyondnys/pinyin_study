"""管理后台仪表盘。"""

from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.practice_book import PracticeBook
from app.models.practice_record import PracticeRecord
from app.models.user import User
from app.models.word_library import WordLibrary
from app.models.wrong_question import WrongQuestion
from app.response import success

router = APIRouter(dependencies=[Depends(require_admin)])


@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    """汇总统计数字。"""
    data = {
        "user_count": db.query(User).filter(User.is_deleted == 0).count(),
        "word_count": db.query(WordLibrary).filter(WordLibrary.is_deleted == 0).count(),
        "book_count": db.query(PracticeBook).filter(PracticeBook.is_deleted == 0).count(),
        "record_count": db.query(PracticeRecord).filter(PracticeRecord.is_deleted == 0).count(),
        "wrong_count": db.query(WrongQuestion).filter(WrongQuestion.is_deleted == 0).count(),
    }
    return success(data)
