"""拼音练习游戏 API。"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_optional_user
from app.response import fail, success
from app.schemas.pinyin_select import AnswerIn, PartAudioOut
from app.services.pinyin_select_service import (
    get_next_question,
    get_part_audio_url,
    get_statistics,
    submit_answer,
)

router = APIRouter()


def _parse_exclude_ids(raw: Optional[str]) -> list[int]:
    if not raw:
        return []
    out: list[int] = []
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit():
            out.append(int(part))
    return out


@router.get("/part-audio")
async def part_audio(
    text: str = Query(..., description="声母或韵母，如 zh、iang；无声母传空由后端读「无」"),
    kind: str = Query("final", description="initial | final"),
    db: Session = Depends(get_db),
    user: Optional[dict] = Depends(get_optional_user),
):
    """点击声母/韵母格子时获取朗读 URL（无则自动生成）。"""
    is_initial = kind.strip().lower() == "initial"
    try:
        url = await get_part_audio_url(db, text, is_initial=is_initial)
    except ValueError as e:
        return fail(1, str(e))
    if not url:
        return fail(1, "暂不支持该拼音部件的朗读")
    # 返回格子上的拼音符号，非 TTS 合成用汉字
    display = text.strip() if text.strip() or not is_initial else "无"
    return success(PartAudioOut(text=display, audio_url=url).model_dump())


@router.get("/question/next")
def question_next(
    session_id: Optional[str] = Query(None, description="游客会话 ID"),
    exclude_ids: Optional[str] = Query(None, description="已答题目 ID，逗号分隔"),
    db: Session = Depends(get_db),
    user: Optional[dict] = Depends(get_optional_user),
):
    """获取下一题（不返回正确答案）。"""
    user_id = user["user_id"] if user else None
    try:
        data = get_next_question(
            db,
            user_id,
            session_id,
            _parse_exclude_ids(exclude_ids),
        )
    except ValueError as e:
        return fail(1, str(e))
    return success(data.model_dump())


@router.post("/answer")
def answer_submit(
    body: AnswerIn,
    db: Session = Depends(get_db),
    user: Optional[dict] = Depends(get_optional_user),
):
    """提交答案，后端判题并记录。"""
    user_id = user["user_id"] if user else None
    try:
        data = submit_answer(db, user_id, body)
    except ValueError as e:
        return fail(1, str(e))
    return success(data.model_dump())


@router.get("/statistics")
def statistics(
    session_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user: Optional[dict] = Depends(get_optional_user),
):
    """答题统计（登录用户按 user_id，游客需传 session_id）。"""
    user_id = user["user_id"] if user else None
    if not user_id and not session_id:
        return fail(1, "请登录或提供 session_id")
    data = get_statistics(db, user_id, session_id)
    return success(data.model_dump())
