"""练习题目模型。"""

from __future__ import annotations

from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import AuditMixin


class PracticeQuestion(Base, AuditMixin):
    """练习册题目表 practice_questions；掌握度 content_id 在拼音场景下即本表 id。"""

    __tablename__ = "practice_questions"

    book_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True,
        comment="所属练习册 ID",
    )
    hanzi: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        comment="题目汉字",
    )
    pinyin: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="题目主读音（声调符号）",
    )
    pinyin_list: Mapped[str] = mapped_column(
        String(512),
        default="[]",
        nullable=False,
        comment="题目全部合法读音 JSON，多音字判题用",
    )
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="册内排序，数值越小越靠前",
    )
