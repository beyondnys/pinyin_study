"""练习与游戏 Schema。"""

from __future__ import annotations
from pydantic import BaseModel
from typing import List


class GameCardOut(BaseModel):
    """游戏宫格卡片（不暴露 pair_key 给前端判题，仅用于展示与本地配对 UX）。"""
    card_id: str
    question_id: int
    card_type: str  # hanzi | pinyin
    text: str


class GameDataOut(BaseModel):
    book_id: int
    book_title: str
    total: int
    cards: List[GameCardOut]


class AnswerItem(BaseModel):
    question_id: int
    user_pinyin: str


class PracticeSubmitRequest(BaseModel):
    book_id: int
    answers: List[AnswerItem]
    duration_seconds: int = 0


class PracticeRecordOut(BaseModel):
    id: int
    book_id: int
    book_title: str
    total_count: int
    correct_count: int
    accuracy: float
    duration_seconds: int

    class Config:
        from_attributes = True


class AnswerDetailOut(BaseModel):
    hanzi: str
    user_pinyin: str
    correct_pinyin: str
    is_correct: bool
