"""字库模型。"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import AuditMixin


class WordLibrary(Base, AuditMixin):
    """汉字拼音字库表 word_libraries。"""

    __tablename__ = "word_libraries"

    hanzi: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        comment="汉字，与 is_deleted 组合唯一",
    )
    pinyin: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="带声调拼音，展示与判题用",
    )
    pinyin_plain: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="无声调拼音，检索与比对用",
    )
    tone: Mapped[Optional[int]] = mapped_column(
        SmallInteger,
        nullable=True,
        comment="声调 1-4，轻声可为空",
    )
    remark: Mapped[str] = mapped_column(
        String(255),
        default="",
        nullable=False,
        comment="备注说明",
    )
