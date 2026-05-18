"""字库 Schema。"""

from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional


class WordCreate(BaseModel):
    hanzi: str
    pinyin: Optional[str] = None
    remark: str = ""


class WordUpdate(BaseModel):
    hanzi: Optional[str] = None
    pinyin: Optional[str] = None
    remark: Optional[str] = None


class WordOut(BaseModel):
    id: int
    hanzi: str
    pinyin: str
    pinyin_list: List[str] = []
    pinyin_plain: str
    remark: str
    hanzi_audio_url: Optional[str] = None
    pinyin_audio_url: Optional[str] = None

    class Config:
        from_attributes = True
