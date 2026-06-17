"""TTS 资源生成、查询与重试。"""

from __future__ import annotations

import asyncio
import logging
import os
import tempfile
from typing import Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from app.config import settings
from app.database import SessionLocal
from app.models.tts_audio_resource import TtsAudioResource
from app.services.minio_audio_service import (
    build_object_name,
    get_presigned_audio_url,
    upload_audio_file,
)
from app.services.tts import tts_biz
from app.services.tts.edge_tts_service import EdgeTTSService
from app.utils.text_hash_util import build_text_hash, normalize_text

logger = logging.getLogger(__name__)


def _get_tts_engine():
    """按配置选择 TTS 引擎（预留扩展）。"""
    if settings.TTS_PROVIDER == "edge":
        return EdgeTTSService()
    raise ValueError(f"不支持的 TTS_PROVIDER: {settings.TTS_PROVIDER}")


def _resolve_voice(voice_name: Optional[str]) -> str:
    v = (voice_name or settings.TTS_DEFAULT_VOICE).strip()
    allowed = {x.strip() for x in settings.TTS_ALLOWED_VOICES.split(",") if x.strip()}
    if v not in allowed:
        return settings.TTS_DEFAULT_VOICE
    return v


async def _sleep_between_tts_items() -> None:
    delay = max(0.0, settings.TTS_BATCH_DELAY_SECONDS)
    if delay:
        await asyncio.sleep(delay)


async def get_or_create_tts_audio(
    db: Session,
    text: str,
    voice_name: Optional[str] = None,
    biz_type: Optional[str] = None,
    biz_id: Optional[int] = None,
    pinyin_text: Optional[str] = None,
    operator_id: Optional[int] = None,
) -> TtsAudioResource:
    """
    获取或创建 TTS 资源：已成功则直接返回；否则生成并上传 MinIO。
    """
    normalized = normalize_text(text)
    if not normalized:
        raise ValueError("TTS 文本不能为空")
    if len(normalized) > settings.TTS_MAX_TEXT_LEN:
        raise ValueError(f"TTS 文本长度不能超过 {settings.TTS_MAX_TEXT_LEN} 字")

    voice = _resolve_voice(voice_name)
    text_hash = build_text_hash(normalized, voice)

    row = (
        db.query(TtsAudioResource)
        .filter(
            TtsAudioResource.text_hash == text_hash,
            TtsAudioResource.voice_name == voice,
            TtsAudioResource.is_deleted == 0,
            TtsAudioResource.enabled_flag == 1,
        )
        .first()
    )
    if row and row.generate_status == tts_biz.GENERATE_SUCCESS:
        row.audio_url = get_presigned_audio_url(row.audio_object_name, row.audio_bucket)
        db.commit()
        return row

    if not row:
        row = TtsAudioResource(
            biz_type=biz_type,
            biz_id=biz_id,
            text_content=normalized,
            text_hash=text_hash,
            pinyin_text=pinyin_text,
            voice_name=voice,
            audio_bucket=settings.MINIO_BUCKET,
            audio_object_name="",
            audio_format="mp3",
            generate_status=tts_biz.GENERATE_RUNNING,
            created_by=operator_id,
            updated_by=operator_id,
        )
        db.add(row)
    else:
        row.biz_type = biz_type or row.biz_type
        row.biz_id = biz_id if biz_id is not None else row.biz_id
        row.pinyin_text = pinyin_text if pinyin_text is not None else row.pinyin_text
        row.generate_status = tts_biz.GENERATE_RUNNING
        row.fail_reason = None
        row.updated_by = operator_id

    db.commit()
    db.refresh(row)

    tmp_path: Optional[str] = None
    try:
        fd, tmp_path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)
        engine = _get_tts_engine()
        await engine.generate_audio(normalized, tmp_path, voice)
        object_name = build_object_name(voice, normalized)
        upload_audio_file(tmp_path, object_name)
        presigned = get_presigned_audio_url(object_name)

        row.audio_object_name = object_name
        row.audio_bucket = settings.MINIO_BUCKET
        row.audio_url = presigned
        row.generate_status = tts_biz.GENERATE_SUCCESS
        row.fail_reason = None
        db.commit()
        db.refresh(row)
        return row
    except Exception as e:
        logger.exception("TTS 生成失败 text=%s", normalized[:32])
        row.generate_status = tts_biz.GENERATE_FAILED
        row.fail_reason = str(e)[:1000]
        row.retry_count = (row.retry_count or 0) + 1
        db.commit()
        db.refresh(row)
        return row
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass


async def retry_tts_audio(db: Session, resource_id: int, operator_id: Optional[int] = None) -> TtsAudioResource:
    """按资源 ID 重试生成。"""
    row = db.query(TtsAudioResource).filter(
        TtsAudioResource.id == resource_id,
        TtsAudioResource.is_deleted == 0,
    ).first()
    if not row:
        raise ValueError("TTS 资源不存在")
    row.retry_count = (row.retry_count or 0) + 1
    db.commit()
    return await get_or_create_tts_audio(
        db,
        text=row.text_content,
        voice_name=row.voice_name,
        biz_type=row.biz_type,
        biz_id=row.biz_id,
        pinyin_text=row.pinyin_text,
        operator_id=operator_id,
    )


def get_presigned_url_for_resource(row: Optional[TtsAudioResource]) -> Optional[str]:
    """成功记录返回新鲜预签名 URL。"""
    if not row or row.generate_status != tts_biz.GENERATE_SUCCESS:
        return None
    if not row.audio_object_name:
        return None
    try:
        return get_presigned_audio_url(row.audio_object_name, row.audio_bucket)
    except Exception:
        logger.exception("预签名失败 id=%s", row.id)
        return row.audio_url


def lookup_audio_urls(
    db: Session,
    pairs: List[Tuple[str, int]],
    voice_name: Optional[str] = None,
) -> Dict[Tuple[str, int], Dict[str, Optional[str]]]:
    """
  批量查询 biz 对应音频 URL。
  pairs: [(biz_type, biz_id), ...]
  返回 {(biz_type, biz_id): {"hanzi": url, "pinyin": url}} 按 biz_type 后缀区分。
    """
    if not pairs:
        return {}
    voice = _resolve_voice(voice_name)
    biz_types = list({p[0] for p in pairs})
    biz_ids = list({p[1] for p in pairs})
    rows = (
        db.query(TtsAudioResource)
        .filter(
            TtsAudioResource.biz_type.in_(biz_types),
            TtsAudioResource.biz_id.in_(biz_ids),
            TtsAudioResource.voice_name == voice,
            TtsAudioResource.generate_status == tts_biz.GENERATE_SUCCESS,
            TtsAudioResource.is_deleted == 0,
            TtsAudioResource.enabled_flag == 1,
        )
        .all()
    )
    by_key: Dict[Tuple[str, int], TtsAudioResource] = {}
    for r in rows:
        if r.biz_type and r.biz_id is not None:
            by_key[(r.biz_type, r.biz_id)] = r

    result: Dict[Tuple[str, int], Dict[str, Optional[str]]] = {}
    hanzi_types = {tts_biz.BIZ_PRACTICE_QUESTION_HANZI, tts_biz.BIZ_PINYIN_WORD_HANZI}
    pinyin_types = {tts_biz.BIZ_PRACTICE_QUESTION_PINYIN, tts_biz.BIZ_PINYIN_WORD_PINYIN}

    # 按 biz_id 聚合 hanzi/pinyin
    by_id: Dict[int, Dict[str, Optional[str]]] = {}
    for (bt, bid), row in by_key.items():
        url = get_presigned_url_for_resource(row)
        slot = by_id.setdefault(bid, {"hanzi": None, "pinyin": None})
        if bt in hanzi_types:
            slot["hanzi"] = url
        elif bt in pinyin_types:
            slot["pinyin"] = url

    for bt, bid in pairs:
        result[(bt, bid)] = by_id.get(bid, {"hanzi": None, "pinyin": None})
    return result


def lookup_word_audio_map(
    db: Session, word_ids: List[int], voice_name: Optional[str] = None
) -> Dict[int, Dict[str, Optional[str]]]:
    """字库 ID -> {hanzi, pinyin} 预签名 URL。"""
    if not word_ids:
        return {}
    voice = _resolve_voice(voice_name)
    out: Dict[int, Dict[str, Optional[str]]] = {wid: {"hanzi": None, "pinyin": None} for wid in word_ids}
    rows = (
        db.query(TtsAudioResource)
        .filter(
            TtsAudioResource.biz_id.in_(word_ids),
            TtsAudioResource.voice_name == voice,
            TtsAudioResource.generate_status == tts_biz.GENERATE_SUCCESS,
            TtsAudioResource.is_deleted == 0,
        )
        .all()
    )
    for r in rows:
        if r.biz_id is None:
            continue
        url = get_presigned_url_for_resource(r)
        slot = out.setdefault(r.biz_id, {"hanzi": None, "pinyin": None})
        if r.biz_type == tts_biz.BIZ_PINYIN_WORD_HANZI:
            slot["hanzi"] = url
        elif r.biz_type == tts_biz.BIZ_PINYIN_WORD_PINYIN:
            slot["pinyin"] = url
    return out


def get_audio_urls_by_texts(
    db: Session, texts: List[str], voice_name: Optional[str] = None
) -> Dict[str, Optional[str]]:
    """按文本内容批量查预签名 URL（用于错题等无 biz_id 场景）。"""
    normalized_list = [normalize_text(t) for t in texts if normalize_text(t)]
    if not normalized_list:
        return {}
    voice = _resolve_voice(voice_name)
    hashes = {build_text_hash(t, voice): t for t in normalized_list}
    rows = (
        db.query(TtsAudioResource)
        .filter(
            TtsAudioResource.text_hash.in_(list(hashes.keys())),
            TtsAudioResource.voice_name == voice,
            TtsAudioResource.generate_status == tts_biz.GENERATE_SUCCESS,
            TtsAudioResource.is_deleted == 0,
        )
        .all()
    )
    out: Dict[str, Optional[str]] = {t: None for t in normalized_list}
    for r in rows:
        orig = hashes.get(r.text_hash)
        if orig:
            out[orig] = get_presigned_url_for_resource(r)
    return out


def lookup_word_match_audio_map(
    db: Session, question_ids: List[int], voice_name: Optional[str] = None
) -> Dict[int, Optional[str]]:
    """词语连连看题目 ID -> 整词 TTS URL。"""
    if not question_ids:
        return {}
    voice = _resolve_voice(voice_name)
    out: Dict[int, Optional[str]] = {qid: None for qid in question_ids}
    rows = (
        db.query(TtsAudioResource)
        .filter(
            TtsAudioResource.biz_id.in_(question_ids),
            TtsAudioResource.biz_type == tts_biz.BIZ_WORD_MATCH_WORD,
            TtsAudioResource.voice_name == voice,
            TtsAudioResource.generate_status == tts_biz.GENERATE_SUCCESS,
            TtsAudioResource.is_deleted == 0,
        )
        .all()
    )
    for r in rows:
        if r.biz_id is not None:
            out[r.biz_id] = get_presigned_url_for_resource(r)
    return out


async def generate_tts_for_word_question(
    db: Session,
    question_id: int,
    word: str,
    pinyin: str,
    operator_id: Optional[int] = None,
) -> None:
    """为词语连连看题目生成整词 TTS + 各单字 TTS（游戏格子朗读用）。"""
    from app.utils.word_split_util import split_word_chars

    try:
        await get_or_create_tts_audio(
            db,
            text=word,
            biz_type=tts_biz.BIZ_WORD_MATCH_WORD,
            biz_id=question_id,
            pinyin_text=pinyin,
            operator_id=operator_id,
        )
    except Exception as e:
        logger.warning("词语整词 TTS 失败 qid=%s: %s", question_id, e)

    for ch in split_word_chars(word):
        try:
            await get_or_create_tts_audio(
                db,
                text=ch,
                biz_type=tts_biz.BIZ_PINYIN_WORD_HANZI,
                biz_id=None,
                operator_id=operator_id,
            )
        except Exception as e:
            logger.warning("词语单字 TTS 失败 qid=%s char=%s: %s", question_id, ch, e)


async def run_tts_background_for_word_questions(
    question_ids: List[int],
    operator_id: Optional[int] = None,
) -> None:
    """后台任务：为词语连连看题目生成 TTS。"""
    if not question_ids:
        return
    db = SessionLocal()
    try:
        from app.models.word_question import WordQuestion

        rows = (
            db.query(WordQuestion)
            .filter(WordQuestion.id.in_(question_ids), WordQuestion.is_deleted == 0)
            .all()
        )
        for q in rows:
            await generate_tts_for_word_question(db, q.id, q.word, q.pinyin, operator_id)
            await _sleep_between_tts_items()
    finally:
        db.close()


def run_tts_background_for_word_questions_sync(
    question_ids: List[int],
    operator_id: Optional[int] = None,
) -> None:
    """同步包装：供 FastAPI BackgroundTasks 可靠触发 asyncio TTS 任务。"""
    import asyncio

    asyncio.run(run_tts_background_for_word_questions(question_ids, operator_id))


def lookup_question_audio_map(
    db: Session, question_ids: List[int], voice_name: Optional[str] = None
) -> Dict[int, Dict[str, Optional[str]]]:
    """题目 ID -> {hanzi_audio_url, pinyin_audio_url}"""
    if not question_ids:
        return {}
    voice = _resolve_voice(voice_name)
    out: Dict[int, Dict[str, Optional[str]]] = {qid: {"hanzi": None, "pinyin": None} for qid in question_ids}
    rows = (
        db.query(TtsAudioResource)
        .filter(
            TtsAudioResource.biz_id.in_(question_ids),
            TtsAudioResource.voice_name == voice,
            TtsAudioResource.generate_status == tts_biz.GENERATE_SUCCESS,
            TtsAudioResource.is_deleted == 0,
        )
        .all()
    )
    for r in rows:
        if r.biz_id is None:
            continue
        url = get_presigned_url_for_resource(r)
        slot = out.setdefault(r.biz_id, {"hanzi": None, "pinyin": None})
        if r.biz_type == tts_biz.BIZ_PRACTICE_QUESTION_HANZI:
            slot["hanzi"] = url
        elif r.biz_type == tts_biz.BIZ_PRACTICE_QUESTION_PINYIN:
            slot["pinyin"] = url
    return out


async def generate_tts_for_question(
    db: Session,
    question_id: int,
    hanzi: str,
    pinyin: str,
    operator_id: Optional[int] = None,
) -> None:
    """为题目生成汉字+拼音两条 TTS（失败不抛出）。"""
    try:
        await get_or_create_tts_audio(
            db,
            text=hanzi,
            biz_type=tts_biz.BIZ_PRACTICE_QUESTION_HANZI,
            biz_id=question_id,
            pinyin_text=pinyin,
            operator_id=operator_id,
        )
    except Exception as e:
        logger.warning("题目汉字 TTS 失败 qid=%s: %s", question_id, e)
    try:
        if pinyin and pinyin.strip():
            await get_or_create_tts_audio(
                db,
                text=pinyin.strip(),
                biz_type=tts_biz.BIZ_PRACTICE_QUESTION_PINYIN,
                biz_id=question_id,
                pinyin_text=pinyin,
                operator_id=operator_id,
            )
    except Exception as e:
        logger.warning("题目拼音 TTS 失败 qid=%s: %s", question_id, e)


async def generate_tts_for_word(
    db: Session,
    word_id: int,
    hanzi: str,
    pinyin: str,
    operator_id: Optional[int] = None,
) -> None:
    """为字库生成汉字+拼音 TTS。"""
    try:
        await get_or_create_tts_audio(
            db,
            text=hanzi,
            biz_type=tts_biz.BIZ_PINYIN_WORD_HANZI,
            biz_id=word_id,
            pinyin_text=pinyin,
            operator_id=operator_id,
        )
    except Exception as e:
        logger.warning("字库汉字 TTS 失败 wid=%s: %s", word_id, e)
    try:
        if pinyin and pinyin.strip():
            await get_or_create_tts_audio(
                db,
                text=pinyin.strip(),
                biz_type=tts_biz.BIZ_PINYIN_WORD_PINYIN,
                biz_id=word_id,
                pinyin_text=pinyin,
                operator_id=operator_id,
            )
    except Exception as e:
        logger.warning("字库拼音 TTS 失败 wid=%s: %s", word_id, e)


async def run_tts_background_for_questions(
    question_ids: List[int],
    operator_id: Optional[int] = None,
) -> None:
    """后台任务：为多个题目生成 TTS。"""
    if not question_ids:
        return
    db = SessionLocal()
    try:
        from app.models.practice_question import PracticeQuestion

        rows = (
            db.query(PracticeQuestion)
            .filter(PracticeQuestion.id.in_(question_ids), PracticeQuestion.is_deleted == 0)
            .all()
        )
        for q in rows:
            await generate_tts_for_question(db, q.id, q.hanzi, q.pinyin, operator_id)
            await _sleep_between_tts_items()
    finally:
        db.close()


async def run_tts_background_for_words(
    word_ids: List[int],
    operator_id: Optional[int] = None,
) -> None:
    """后台任务：为字库条目生成 TTS。"""
    if not word_ids:
        return
    db = SessionLocal()
    try:
        from app.models.word_library import WordLibrary

        rows = (
            db.query(WordLibrary)
            .filter(WordLibrary.id.in_(word_ids), WordLibrary.is_deleted == 0)
            .all()
        )
        for w in rows:
            await generate_tts_for_word(db, w.id, w.hanzi, w.pinyin, operator_id)
            await _sleep_between_tts_items()
    finally:
        db.close()
