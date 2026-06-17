"""词语连连看题目模型。"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import BigInteger, Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import AuditMixin


class WordQuestion(Base, AuditMixin):
    """词语连连看题目表 word_questions。"""

    __tablename__ = "word_questions"

    book_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True,
        comment="所属词库 ID",
    )
    word: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        comment="完整词语，2～4 字",
    )
    pinyin: Mapped[str] = mapped_column(
        String(128),
        default="",
        nullable=False,
        comment="整词拼音（带调）",
    )
    pinyin_list: Mapped[str] = mapped_column(
        String(512),
        default="[]",
        nullable=False,
        comment="多音 JSON，预留",
    )
    word_len: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        comment="字数 2～4",
    )
    meaning: Mapped[Optional[str]] = mapped_column(
        String(256),
        nullable=True,
        comment="释义，预留对接外部 API",
    )
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="册内排序",
    )
