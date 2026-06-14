"""拼音练习游戏（选声母/韵母/声调）服务。"""

from __future__ import annotations

import random
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.pinyin_game_record import PinyinGameRecord
from app.models.pinyin_question import PinyinQuestion
from app.schemas.pinyin_select import AnswerIn, AnswerOut, NextQuestionOut, StatisticsOut
from app.services.tts import tts_biz
from app.services.tts.tts_audio_service import get_audio_urls_by_texts, get_or_create_tts_audio
from app.services.wrong_question_service import upsert_wrong_questions
from app.utils.pinyin_part_tts_util import part_to_tts_speak_text

SCORE_PER_CORRECT = 10


async def get_part_audio_url(db: Session, text: str, *, is_initial: bool = False) -> Optional[str]:
    """
    获取声母/韵母读音（MinIO 预签名 URL）。
    无缓存时现场 edge-tts 生成并入库（TTS 文本为汉语认读字，非拉丁字母）。
    """
    speak_text = part_to_tts_speak_text(text, is_initial=is_initial)
    if not speak_text:
        return None
    part_key = (text or "").strip()
    row = await get_or_create_tts_audio(
        db,
        speak_text,
        biz_type=tts_biz.BIZ_PINYIN_SELECT_PART,
        pinyin_text=part_key or None,
    )
    return row.audio_url


def _norm_initial(value: str) -> str:
    return (value or "").strip()


def _norm_final(value: str) -> str:
    return (value or "").strip().lower().replace("ü", "v")


def is_answer_correct(q: PinyinQuestion, initial: str, final: str, tone: int) -> bool:
    """声母、韵母、声调须与题库完全一致。"""
    return (
        _norm_initial(initial) == _norm_initial(q.initial)
        and _norm_final(final) == _norm_final(q.final)
        and int(tone) == int(q.tone)
    )


def _session_filter(q, user_id: Optional[int], session_id: Optional[str]):
    if user_id:
        return q.filter(PinyinGameRecord.user_id == user_id)
    if session_id:
        return q.filter(PinyinGameRecord.session_id == session_id)
    return q.filter(PinyinGameRecord.id == -1)


def _total_score(db: Session, user_id: Optional[int], session_id: Optional[str]) -> int:
    q = db.query(func.coalesce(func.sum(PinyinGameRecord.score_delta), 0))
    q = _session_filter(q, user_id, session_id)
    return int(q.scalar() or 0)


def _index_no(db: Session, user_id: Optional[int], session_id: Optional[str]) -> int:
    q = db.query(func.count(PinyinGameRecord.id))
    q = _session_filter(q, user_id, session_id)
    return int(q.scalar() or 0) + 1


def get_next_question(
    db: Session,
    user_id: Optional[int],
    session_id: Optional[str],
    exclude_ids: list[int],
) -> NextQuestionOut:
    """随机一题，不返回答案字段。"""
    q = db.query(PinyinQuestion).filter(
        PinyinQuestion.is_deleted == 0,
        PinyinQuestion.status == 1,
    )
    if exclude_ids:
        q = q.filter(PinyinQuestion.id.notin_(exclude_ids))
    rows = q.all()
    if not rows:
        raise ValueError("题库为空，请先执行 SQL 迁移并运行 sync_pinyin_questions")
    picked = random.choice(rows)
    audio_map = get_audio_urls_by_texts(db, [picked.hanzi])
    return NextQuestionOut(
        question_id=picked.id,
        hanzi=picked.hanzi,
        audio_url=audio_map.get(picked.hanzi),
        index_no=_index_no(db, user_id, session_id),
        zero_initial=not bool(_norm_initial(picked.initial)),
    )


def submit_answer(
    db: Session,
    user_id: Optional[int],
    body: AnswerIn,
) -> AnswerOut:
    """判题、记分、写记录；答错写入错题本。"""
    question = (
        db.query(PinyinQuestion)
        .filter(
            PinyinQuestion.id == body.question_id,
            PinyinQuestion.is_deleted == 0,
            PinyinQuestion.status == 1,
        )
        .first()
    )
    if not question:
        raise ValueError("题目不存在")

    ok = is_answer_correct(question, body.initial, body.final, body.tone)
    score_delta = SCORE_PER_CORRECT if ok else 0
    session_id = (body.session_id or "").strip() or None

    record = PinyinGameRecord(
        user_id=user_id,
        session_id=session_id,
        question_id=question.id,
        hanzi=question.hanzi,
        user_initial=_norm_initial(body.initial),
        user_final=_norm_final(body.final),
        user_tone=int(body.tone),
        is_correct=1 if ok else 0,
        duration_ms=body.duration_ms,
        score_delta=score_delta,
        created_by=user_id,
        updated_by=user_id,
    )
    db.add(record)

    if not ok and user_id:
        upsert_wrong_questions(
            db,
            user_id,
            [(question.hanzi, question.pinyin_display, 0)],
        )

    db.commit()

    total_score = _total_score(db, user_id, session_id)
    return AnswerOut(
        is_correct=ok,
        score_delta=score_delta,
        total_score=total_score,
        correct_initial=question.initial,
        correct_final=question.final,
        correct_tone=question.tone,
        pinyin_display=question.pinyin_display,
        hanzi=question.hanzi,
    )


def get_statistics(
    db: Session,
    user_id: Optional[int],
    session_id: Optional[str],
) -> StatisticsOut:
    """按用户或游客会话统计本场数据。"""
    if not user_id and not session_id:
        return StatisticsOut(total_count=0, correct_count=0, accuracy=0.0, total_score=0)

    base = db.query(PinyinGameRecord).filter(PinyinGameRecord.is_deleted == 0)
    if user_id:
        base = base.filter(PinyinGameRecord.user_id == user_id)
    else:
        base = base.filter(PinyinGameRecord.session_id == session_id)

    total = base.count()
    correct = base.filter(PinyinGameRecord.is_correct == 1).count()
    accuracy = round(correct / total * 100, 2) if total else 0.0
    total_score = _total_score(db, user_id, session_id)
    return StatisticsOut(
        total_count=total,
        correct_count=correct,
        accuracy=accuracy,
        total_score=total_score,
    )
