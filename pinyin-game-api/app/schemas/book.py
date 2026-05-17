"""练习册 Schema。"""

from __future__ import annotations
from pydantic import BaseModel
from typing import Optional


class BookCreate(BaseModel):
    title: str
    description: str = ""
    status: int = 1


class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None


class BookOut(BaseModel):
    id: int
    title: str
    description: str
    question_count: int
    status: int

    class Config:
        from_attributes = True
