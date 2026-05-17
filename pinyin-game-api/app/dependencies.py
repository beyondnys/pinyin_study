"""FastAPI 依赖：鉴权与权限。"""

from __future__ import annotations

from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.utils.jwt_util import decode_token
from app.utils.redis_util import get_login_token

security = HTTPBearer(auto_error=False)


def get_current_user(
    creds: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> dict:
    """
    校验 Bearer Token：JWT 合法且 Redis 中存在会话。
    返回合并后的用户信息字典。
    """
    if not creds or not creds.credentials:
        raise HTTPException(status_code=401, detail="未登录")
    token = creds.credentials
    try:
        claims = decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="无效或过期的登录凭证")
    session = get_login_token(token)
    if not session:
        raise HTTPException(status_code=401, detail="登录已失效，请重新登录")
    return {
        "user_id": int(claims["sub"]),
        "username": claims.get("username") or session.get("username"),
        "role": claims.get("role") or session.get("role"),
        "token": token,
    }


def require_admin(user: dict = Depends(get_current_user)) -> dict:
    """要求管理员角色。"""
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return user
