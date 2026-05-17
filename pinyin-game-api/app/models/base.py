"""模型基类：统一审计字段。"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, SmallInteger, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AuditMixin:
    """审计字段混入类，所有业务表均包含以下列。"""

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="主键，自增",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
        comment="记录创建时间",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="记录最后更新时间",
    )
    created_by: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        nullable=True,
        comment="创建人用户 ID，系统脚本可为空",
    )
    updated_by: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        nullable=True,
        comment="最后修改人用户 ID",
    )
    is_deleted: Mapped[int] = mapped_column(
        SmallInteger,
        default=0,
        nullable=False,
        comment="软删除：0 正常，1 已删除",
    )
