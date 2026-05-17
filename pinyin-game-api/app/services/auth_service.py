"""认证服务：登录、登出。"""

from __future__ import annotations

from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app.config import settings
from app.models.user import User
from app.utils.jwt_util import create_access_token
from app.utils.password_util import hash_password, verify_password
from app.utils.redis_util import revoke_all_user_tokens, revoke_token, save_login_token


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """按用户名查询未删除用户。"""
    return (
        db.query(User)
        .filter(User.username == username, User.is_deleted == 0)
        .first()
    )


def register_student(
    db: Session,
    username: str,
    password: str,
    nickname: str = "",
) -> User:
    """
    前台学生注册：固定 role=student，禁止占用 admin 用户名。
    """
    name = username.strip()
    if not name:
        raise ValueError("用户名不能为空")
    if name.lower() == "admin":
        raise ValueError("该用户名不可注册")
    if get_user_by_username(db, name):
        raise ValueError("用户名已存在")

    display = (nickname or name).strip()[:64]
    user = User(
        username=name,
        password_hash=hash_password(password),
        nickname=display,
        role="student",
        status=1,
        created_by=None,
        updated_by=None,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login(db: Session, username: str, password: str) -> Tuple[str, User]:
    """
    校验密码并签发 Token，写入 Redis。
    返回 (token, user)。
    """
    user = get_user_by_username(db, username)
    if not user or user.status != 1:
        raise ValueError("用户名或密码错误")
    if not verify_password(password, user.password_hash):
        raise ValueError("用户名或密码错误")

    if settings.SINGLE_LOGIN:
        revoke_all_user_tokens(user.id)

    token = create_access_token(user.id, user.username, user.role)
    payload = {"user_id": user.id, "username": user.username, "role": user.role}
    ttl = settings.JWT_EXPIRE_DAYS * 86400
    save_login_token(token, payload, ttl)
    return token, user


def logout(token: str, user_id: int) -> None:
    """退出登录，删除 Redis 中的 token。"""
    revoke_token(token, user_id)
