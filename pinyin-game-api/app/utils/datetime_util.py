"""日期时间工具。"""

from __future__ import annotations
from datetime import datetime, timezone


def utc_now() -> datetime:
    """返回当前 UTC 时间（无时区信息，便于存 MySQL）。"""
    return datetime.now(timezone.utc).replace(tzinfo=None)
