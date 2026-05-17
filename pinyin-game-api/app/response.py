"""统一 API 响应结构。"""

from __future__ import annotations
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """标准响应：code=0 成功。"""

    code: int = 0
    message: str = "ok"
    data: Optional[T] = None


def success(data: Any = None, message: str = "ok") -> dict:
    """构造成功响应字典。"""
    return {"code": 0, "message": message, "data": data}


def fail(code: int = 1, message: str = "error", data: Any = None) -> dict:
    """构造失败响应字典。"""
    return {"code": code, "message": message, "data": data}
