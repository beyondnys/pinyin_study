"""错题 Schema。"""

from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime


class WrongQuestionOut(BaseModel):
    id: int
    book_id: int
    hanzi: str
    pinyin: str
    wrong_count: int
    last_wrong_at: datetime

    class Config:
        from_attributes = True
