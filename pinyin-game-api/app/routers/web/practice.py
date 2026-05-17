"""前台练习提交与结果。"""

from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.practice_answer_detail import PracticeAnswerDetail
from app.models.practice_book import PracticeBook
from app.models.practice_record import PracticeRecord
from app.response import fail, success
from app.schemas.practice import PracticeSubmitRequest
from app.services.practice_service import submit_practice

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/submit")
def submit(body: PracticeSubmitRequest, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """提交练习答案。"""
    if not body.answers:
        return fail(1, "答案不能为空")
    try:
        record = submit_practice(
            db, user["user_id"], body.book_id, body.answers, body.duration_seconds
        )
    except ValueError as e:
        return fail(1, str(e))
    book = db.query(PracticeBook).filter(PracticeBook.id == body.book_id).first()
    return success(
        {
            "record_id": record.id,
            "book_title": book.title if book else "",
            "total_count": record.total_count,
            "correct_count": record.correct_count,
            "accuracy": float(record.accuracy),
            "duration_seconds": record.duration_seconds,
        }
    )


@router.get("/records/{record_id}")
def get_record(record_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """获取练习结果与明细。"""
    record = (
        db.query(PracticeRecord)
        .filter(
            PracticeRecord.id == record_id,
            PracticeRecord.user_id == user["user_id"],
            PracticeRecord.is_deleted == 0,
        )
        .first()
    )
    if not record:
        return fail(1, "记录不存在")
    book = db.query(PracticeBook).filter(PracticeBook.id == record.book_id).first()
    details = (
        db.query(PracticeAnswerDetail)
        .filter(PracticeAnswerDetail.record_id == record_id, PracticeAnswerDetail.is_deleted == 0)
        .all()
    )
    return success(
        {
            "id": record.id,
            "book_id": record.book_id,
            "book_title": book.title if book else "",
            "total_count": record.total_count,
            "correct_count": record.correct_count,
            "accuracy": float(record.accuracy),
            "duration_seconds": record.duration_seconds,
            "details": [
                {
                    "hanzi": d.hanzi,
                    "user_pinyin": d.user_pinyin,
                    "correct_pinyin": d.correct_pinyin,
                    "is_correct": bool(d.is_correct),
                }
                for d in details
            ],
        }
    )
