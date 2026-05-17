"""答题明细模型。"""

from __future__ import annotations

from sqlalchemy import BigInteger, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import AuditMixin


class PracticeAnswerDetail(Base, AuditMixin):
    """答题明细表 practice_answer_details，一次练习下每题一条。"""

    __tablename__ = "practice_answer_details"

    record_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True,
        comment="关联 practice_records.id",
    )
    question_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="题目 ID，对应 practice_questions.id",
    )
    hanzi: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        comment="题目汉字快照",
    )
    user_pinyin: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="用户提交的拼音",
    )
    correct_pinyin: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="标准拼音快照",
    )
    is_correct: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        comment="是否答对：1 对，0 错",
    )
