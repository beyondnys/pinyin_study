"""词语连连看答题明细模型。"""

from __future__ import annotations

from sqlalchemy import BigInteger, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import AuditMixin


class WordMatchAnswerDetail(Base, AuditMixin):
    """词语连连看答题明细表 word_match_answer_details。"""

    __tablename__ = "word_match_answer_details"

    record_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True,
        comment="关联 word_match_records.id",
    )
    question_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="word_questions.id",
    )
    word: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        comment="词语快照",
    )
    is_correct: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        comment="1 连对 0 错",
    )
