"""用户模型。"""

from __future__ import annotations

from sqlalchemy import Enum, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import AuditMixin


class User(Base, AuditMixin):
    """系统用户表 users：管理员 admin / 学生 student。"""

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="登录用户名，与 is_deleted 组合唯一",
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="bcrypt 密码哈希，明文不落库",
    )
    nickname: Mapped[str] = mapped_column(
        String(64),
        default="",
        nullable=False,
        comment="显示昵称",
    )
    role: Mapped[str] = mapped_column(
        Enum("admin", "student", name="user_role"),
        default="student",
        comment="角色：admin 管理端，student 学生端",
    )
    status: Mapped[int] = mapped_column(
        SmallInteger,
        default=1,
        nullable=False,
        comment="账号状态：1 启用，0 禁用",
    )
