"""JWT 工具：签发与解析。"""

from __future__ import annotations
import uuid
from datetime import datetime, timedelta, timezone

import jwt

from app.config import settings


def create_access_token(user_id: int, username: str, role: str) -> str:
    """生成 JWT，携带用户基本信息。"""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "jti": str(uuid.uuid4()),
        "exp": now + timedelta(days=settings.JWT_EXPIRE_DAYS),
        "iat": now,
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")


def decode_token(token: str) -> dict:
    """解析 JWT，失败则抛出 jwt 异常。"""
    return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
