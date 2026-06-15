"""前台词语连连看提交与结果。"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.word_book import WordBook
from app.models.word_match_answer_detail import WordMatchAnswerDetail
from app.models.word_match_record import WordMatchRecord
from app.response import fail, success
from app.schemas.word_match import WordMatchSubmitRequest, WordMatchWrongAttemptRequest
from app.services.word_match_service import record_word_wrong_attempt, submit_word_match

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/submit")
def submit(body: WordMatchSubmitRequest, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """提交词语连连看成绩。"""
    if not body.answers:
        return fail(1, "请先完成连词再提交")
    try:
        record = submit_word_match(
            db, user["user_id"], body.book_id, body.answers, body.duration_seconds
        )
    except ValueError as e:
        return fail(1, str(e))
    book = db.query(WordBook).filter(WordBook.id == body.book_id).first()
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


@router.post("/wrong-attempt")
def wrong_attempt(
    body: WordMatchWrongAttemptRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """连字顺序错误时记入错题本与掌握度。"""
    ok = record_word_wrong_attempt(db, user["user_id"], body.book_id, body.question_id)
    if not ok:
        return fail(1, "题目不存在")
    return success({"recorded": True})


@router.get("/records/{record_id}")
def get_record(record_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """获取词语连连看结果与明细。"""
    record = (
        db.query(WordMatchRecord)
        .filter(
            WordMatchRecord.id == record_id,
            WordMatchRecord.user_id == user["user_id"],
            WordMatchRecord.is_deleted == 0,
        )
        .first()
    )
    if not record:
        return fail(1, "记录不存在")
    book = db.query(WordBook).filter(WordBook.id == record.book_id).first()
    details = (
        db.query(WordMatchAnswerDetail)
        .filter(WordMatchAnswerDetail.record_id == record_id, WordMatchAnswerDetail.is_deleted == 0)
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
                    "word": d.word,
                    "is_correct": bool(d.is_correct),
                }
                for d in details
            ],
        }
    )
