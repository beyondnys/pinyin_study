"""认证相关 Schema。"""

from __future__ import annotations
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=64)
    password: str = Field(..., min_length=1, max_length=128)


class RegisterRequest(BaseModel):
    """前台学生自助注册。"""

    username: str = Field(..., min_length=2, max_length=64, description="登录用户名")
    password: str = Field(..., min_length=6, max_length=128, description="密码至少 6 位")
    nickname: str = Field(default="", max_length=64, description="昵称，为空则用用户名")


class LoginResponse(BaseModel):
    token: str
    user_id: int
    username: str
    nickname: str
    role: str


class UserInfo(BaseModel):
    user_id: int
    username: str
    nickname: str
    role: str
