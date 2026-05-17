"""业务异常定义。"""

from __future__ import annotations
from fastapi import HTTPException


class BusinessException(HTTPException):
    """可预期的业务错误，映射为 HTTP 400。"""

    def __init__(self, message: str, code: int = 1):
        super().__init__(status_code=400, detail={"code": code, "message": message})
