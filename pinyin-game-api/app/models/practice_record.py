"""学习记录模型。"""

from __future__ import annotations

from sqlalchemy import BigInteger, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import AuditMixin


class PracticeRecord(Base, AuditMixin):
    """练习汇总表 practice_records，一次完成并提交对应一条记录。"""

    __tablename__ = "practice_records"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True,
        comment="练习学生用户 ID",
    )
    book_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="练习册 ID",
    )
    total_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="本次提交题目总数",
    )
    correct_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="本次答对题数",
    )
    accuracy: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        comment="正确率百分比，如 87.50",
    )
    duration_seconds: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="本次练习耗时，单位秒",
    )
