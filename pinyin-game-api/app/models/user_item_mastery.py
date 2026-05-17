"""用户内容掌握度（自适应抽题），与错题本独立。"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, Integer, SmallInteger, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import AuditMixin


class UserItemMastery(Base, AuditMixin):
    """
    掌握度表 user_item_mastery。
    粒度：用户 + 内容类型 + 内容 ID + 场景(scope)。
    用于加权抽题、连续答对 streak、复习间隔 next_review_at。
    """

    __tablename__ = "user_item_mastery"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "content_type",
            "content_id",
            "scope_type",
            "scope_id",
            "is_deleted",
            name="uk_user_content_scope",
        ),
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True,
        comment="学生用户 ID",
    )
    content_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        comment="内容类型：pinyin_pair / word_choice / idiom_choice 等",
    )
    content_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="业务主键，拼音场景为 practice_questions.id",
    )
    scope_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        comment="场景类型，如 book、global",
    )
    scope_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="场景 ID，如练习册 book_id",
    )
    state: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        default="unseen",
        comment="掌握状态：unseen 未练 / learning 学习中 / mastered 已掌握",
    )
    wrong_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="历史累计答错次数，每次判错加 1",
    )
    correct_streak: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="当前连续答对次数，答错清零",
    )
    total_attempts: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="累计作答次数，每记录一题加 1",
    )
    last_result: Mapped[Optional[int]] = mapped_column(
        SmallInteger,
        nullable=True,
        comment="最近一次结果：1 对，0 错，未答过为空",
    )
    last_wrong_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="最近一次答错时间",
    )
    last_correct_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="最近一次答对时间",
    )
    last_practiced_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="最近一次练习时间，对或错均更新",
    )
    next_review_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="下次建议复习时间，到期后抽题权重升高",
    )
