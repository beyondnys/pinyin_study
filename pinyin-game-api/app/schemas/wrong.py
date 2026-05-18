"""错题 Schema。"""

from __future__ import annotations
from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class WrongAttemptIn(BaseModel):
    """配对游戏答错时上报（汉字题 id + 用户误选的拼音）。"""

    book_id: int = 0
    question_id: int
    user_pinyin: str


class WrongQuestionOut(BaseModel):
    id: int
    book_id: int
    hanzi: str
    pinyin: str
    wrong_count: int
    last_wrong_at: datetime
    hanzi_audio_url: Optional[str] = None
    pinyin_audio_url: Optional[str] = None

    class Config:
        from_attributes = True
