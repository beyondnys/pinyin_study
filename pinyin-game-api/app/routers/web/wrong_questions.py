"""前台错题本。"""

from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.wrong_question import WrongQuestion
from app.response import success
from app.schemas.wrong import WrongAttemptIn, WrongQuestionOut
from app.services.practice_service import record_wrong_pair_attempt
from app.services.tts.tts_audio_service import get_audio_urls_by_texts

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/attempt")
def record_wrong_attempt(
    body: WrongAttemptIn,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """配对游戏选错时即时记入错题本（无需等点击「完成」）。"""
    record_wrong_pair_attempt(
        db,
        user_id=user["user_id"],
        book_id=body.book_id,
        question_id=body.question_id,
        user_pinyin=body.user_pinyin,
    )
    return success(None)


@router.get("")
def my_wrong_questions(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """当前用户错题列表。"""
    items = (
        db.query(WrongQuestion)
        .filter(WrongQuestion.user_id == user["user_id"], WrongQuestion.is_deleted == 0)
        .order_by(WrongQuestion.last_wrong_at.desc())
        .all()
    )
    hanzi_texts = [w.hanzi for w in items]
    pinyin_texts = [w.pinyin for w in items]
    hanzi_urls = get_audio_urls_by_texts(db, hanzi_texts)
    pinyin_urls = get_audio_urls_by_texts(db, pinyin_texts)
    out = []
    for w in items:
        row = WrongQuestionOut.model_validate(w).model_dump()
        row["hanzi_audio_url"] = hanzi_urls.get(w.hanzi)
        row["pinyin_audio_url"] = pinyin_urls.get(w.pinyin)
        out.append(row)
    return success(out)
