"""错题本模型。"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import AuditMixin


class WrongQuestion(Base, AuditMixin):
    """
    错题本表 wrong_questions。
    与 user_item_mastery 独立：面向错题展示与运营，不参与加权抽题。
    """

    __tablename__ = "wrong_questions"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True,
        comment="学生用户 ID",
    )
    book_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="关联练习册 ID，便于按册查看",
    )
    hanzi: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        comment="错题汉字",
    )
    pinyin: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="正确拼音",
    )
    wrong_count: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
        comment="累计答错次数，每次提交判错加 1",
    )
    last_wrong_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        comment="最近一次答错时间",
    )
