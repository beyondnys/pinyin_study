"""TTS Schema。"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class TtsAudioOut(BaseModel):
    id: int
    biz_type: Optional[str] = None
    biz_id: Optional[int] = None
    text_content: str
    pinyin_text: Optional[str] = None
    voice_name: str
    audio_url: Optional[str] = None
    audio_format: str
    generate_status: int
    fail_reason: Optional[str] = None
    retry_count: int

    class Config:
        from_attributes = True


class TtsRetryByBizRequest(BaseModel):
    biz_type: str = Field(..., description="业务类型")
    biz_id: int = Field(..., description="业务 ID")
    voice_name: Optional[str] = None


class TtsBackfillRequest(BaseModel):
    """管理端触发回填（可选过滤）。"""
    scope: str = Field("all", description="all | questions | words")
    limit: int = Field(500, ge=1, le=5000)
