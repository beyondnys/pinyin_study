"""Redis 工具：登录 Token 与会话管理。"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

import redis

from app.config import settings

_redis_client: Optional[redis.Redis] = None


def get_redis() -> redis.Redis:
    """获取 Redis 客户端单例。"""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis_client


def save_login_token(token: str, payload: Dict[str, Any], ttl_seconds: int) -> None:
    """保存登录会话到 Redis。"""
    r = get_redis()
    key = f"login:token:{token}"
    r.setex(key, ttl_seconds, json.dumps(payload, ensure_ascii=False))
    uid = payload["user_id"]
    r.sadd(f"user:tokens:{uid}", token)


def get_login_token(token: str) -> Optional[Dict[str, Any]]:
    """读取登录会话，不存在返回 None。"""
    raw = get_redis().get(f"login:token:{token}")
    if not raw:
        return None
    return json.loads(raw)


def revoke_token(token: str, user_id: int) -> None:
    """删除单个 token。"""
    r = get_redis()
    r.delete(f"login:token:{token}")
    r.srem(f"user:tokens:{user_id}", token)


def revoke_all_user_tokens(user_id: int) -> None:
    """删除用户全部 token（单点登录）。"""
    r = get_redis()
    tokens = r.smembers(f"user:tokens:{user_id}")
    for t in tokens:
        r.delete(f"login:token:{t}")
    r.delete(f"user:tokens:{user_id}")
