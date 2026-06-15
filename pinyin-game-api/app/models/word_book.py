"""词语连连看词库模型。"""

from __future__ import annotations

from sqlalchemy import Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import AuditMixin


class WordBook(Base, AuditMixin):
    """词语连连看词库表 word_books。"""

    __tablename__ = "word_books"

    title: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        comment="词库标题",
    )
    description: Mapped[str] = mapped_column(
        String(512),
        default="",
        nullable=False,
        comment="词库描述",
    )
    question_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="题目数量冗余",
    )
    status: Mapped[int] = mapped_column(
        SmallInteger,
        default=1,
        nullable=False,
        comment="1 启用 0 下架",
    )
