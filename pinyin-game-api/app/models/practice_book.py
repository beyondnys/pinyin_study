"""练习册模型。"""

from __future__ import annotations

from sqlalchemy import Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import AuditMixin


class PracticeBook(Base, AuditMixin):
    """练习册表 practice_books。"""

    __tablename__ = "practice_books"

    title: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        comment="练习册标题",
    )
    description: Mapped[str] = mapped_column(
        String(512),
        default="",
        nullable=False,
        comment="练习册描述",
    )
    question_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="题目数量冗余字段，增删题时由业务维护",
    )
    status: Mapped[int] = mapped_column(
        SmallInteger,
        default=1,
        nullable=False,
        comment="上架状态：1 启用前台可见，0 下架",
    )
