"""密码哈希与校验（使用 bcrypt，兼容 passlib 生成的 $2b$ 哈希）。"""

from __future__ import annotations

import bcrypt


def hash_password(plain: str) -> str:
    """对明文密码进行 bcrypt 哈希。"""
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """校验明文与哈希是否匹配。"""
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except (ValueError, TypeError):
        return False
