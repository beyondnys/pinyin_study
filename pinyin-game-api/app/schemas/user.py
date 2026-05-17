"""用户 Schema。"""

from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str
    nickname: str = ""
    role: str = "student"
    status: int = 1


class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    status: Optional[int] = None


class UserOut(BaseModel):
    id: int
    username: str
    nickname: str
    role: str
    status: int

    class Config:
        from_attributes = True
