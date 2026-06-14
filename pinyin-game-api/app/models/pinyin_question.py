"""拼音练习游戏题库。"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import BigInteger, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import AuditMixin


class PinyinQuestion(Base, AuditMixin):
    """拼音选拼题目表 pinyin_question。"""

    __tablename__ = "pinyin_question"

    source_type: Mapped[Optional[str]] = mapped_column(
        String(32),
        nullable=True,
        comment="来源类型",
    )
    source_id: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        nullable=True,
        comment="来源主键",
    )
    hanzi: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        index=True,
        comment="汉字",
    )
    initial: Mapped[str] = mapped_column(
        String(16),
        default="",
        nullable=False,
        comment="标准声母",
    )
    final: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        comment="标准韵母",
    )
    tone: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        comment="标准声调 1-5",
    )
    pinyin_display: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="带调完整拼音",
    )
    status: Mapped[int] = mapped_column(
        SmallInteger,
        default=1,
        nullable=False,
        comment="1 启用 0 停用",
    )
