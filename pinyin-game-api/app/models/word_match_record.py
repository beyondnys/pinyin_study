"""词语连连看练习记录模型。"""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy import BigInteger, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import AuditMixin


class WordMatchRecord(Base, AuditMixin):
    """词语连连看练习记录表 word_match_records。"""

    __tablename__ = "word_match_records"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True,
        comment="学生用户 ID",
    )
    book_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="词库 ID",
    )
    total_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="本轮词语总数",
    )
    correct_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="连对词语数",
    )
    accuracy: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        comment="正确率",
    )
    duration_seconds: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="耗时秒",
    )
