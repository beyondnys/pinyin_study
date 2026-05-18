"""TTS 管理接口：查询、重试。"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.tts_audio_resource import TtsAudioResource
from app.response import fail, success
from app.schemas.tts_schema import TtsAudioOut, TtsRetryByBizRequest
from app.services.tts import tts_biz
from app.services.tts.tts_audio_service import (
    get_or_create_tts_audio,
    get_presigned_url_for_resource,
    retry_tts_audio,
)

router = APIRouter(dependencies=[Depends(require_admin)])


def _to_out(row: TtsAudioResource) -> dict:
    data = TtsAudioOut.model_validate(row).model_dump()
    data["audio_url"] = get_presigned_url_for_resource(row)
    return data


@router.get("/{resource_id}")
async def get_tts_resource(resource_id: int, db: Session = Depends(get_db)):
    """查询单条 TTS 资源。"""
    row = db.query(TtsAudioResource).filter(
        TtsAudioResource.id == resource_id,
        TtsAudioResource.is_deleted == 0,
    ).first()
    if not row:
        return fail(1, "资源不存在")
    return success(_to_out(row))


@router.post("/{resource_id}/retry")
async def retry_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin),
):
    """按 ID 重试生成。"""
    try:
        row = await retry_tts_audio(db, resource_id, admin.get("user_id"))
    except ValueError as e:
        return fail(1, str(e))
    return success(_to_out(row))


@router.post("/retry-by-biz")
async def retry_by_biz(
    body: TtsRetryByBizRequest,
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin),
):
    """按业务类型与 ID 重试（需已有记录或提供文本）。"""
    row = (
        db.query(TtsAudioResource)
        .filter(
            TtsAudioResource.biz_type == body.biz_type,
            TtsAudioResource.biz_id == body.biz_id,
            TtsAudioResource.is_deleted == 0,
        )
        .order_by(TtsAudioResource.id.desc())
        .first()
    )
    if not row:
        return fail(1, "未找到 TTS 记录，请先导入文本或执行回填脚本")
    if row.generate_status == tts_biz.GENERATE_SUCCESS:
        row.audio_url = get_presigned_url_for_resource(row)
        return success(_to_out(row))
    row = await retry_tts_audio(db, row.id, admin.get("user_id"))
    return success(_to_out(row))
