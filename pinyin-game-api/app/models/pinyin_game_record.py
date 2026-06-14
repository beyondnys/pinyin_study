"""拼音练习游戏答题记录。"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import BigInteger, Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import AuditMixin


class PinyinGameRecord(Base, AuditMixin):
    """拼音选拼答题记录表 pinyin_game_record。"""

    __tablename__ = "pinyin_game_record"

    user_id: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        nullable=True,
        index=True,
        comment="用户 ID，未登录为空",
    )
    session_id: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
        index=True,
        comment="游客会话 ID",
    )
    question_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True,
        comment="题目 ID",
    )
    hanzi: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        comment="汉字",
    )
    user_initial: Mapped[str] = mapped_column(
        String(16),
        default="",
        nullable=False,
        comment="用户所选声母",
    )
    user_final: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        comment="用户所选韵母",
    )
    user_tone: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        comment="用户所选声调",
    )
    is_correct: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        comment="是否正确 1/0",
    )
    duration_ms: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="答题耗时毫秒",
    )
    score_delta: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="本题得分变化",
    )
