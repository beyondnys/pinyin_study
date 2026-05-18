"""TTS 语音资源模型。"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import BigInteger, Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import AuditMixin


class TtsAudioResource(Base, AuditMixin):
    """tts_audio_resource 表：文本对应 MinIO 音频资源。"""

    __tablename__ = "tts_audio_resource"

    biz_type: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, comment="业务类型")
    biz_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, comment="业务 ID")
    text_content: Mapped[str] = mapped_column(String(1000), nullable=False, comment="TTS 文本")
    text_hash: Mapped[str] = mapped_column(String(64), nullable=False, comment="文本 hash")
    pinyin_text: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True, comment="关联拼音")
    voice_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="zh-CN-XiaoxiaoNeural",
        comment="TTS 音色",
    )
    audio_bucket: Mapped[str] = mapped_column(String(100), nullable=False, comment="MinIO bucket")
    audio_object_name: Mapped[str] = mapped_column(String(500), nullable=False, comment="对象路径")
    audio_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True, comment="最近预签名 URL")
    audio_format: Mapped[str] = mapped_column(String(20), nullable=False, default="mp3", comment="格式")
    generate_status: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        default=0,
        comment="0待生成 1生成中 2成功 3失败",
    )
    fail_reason: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True, comment="失败原因")
    retry_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="重试次数")
    enabled_flag: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1, comment="1启用")
