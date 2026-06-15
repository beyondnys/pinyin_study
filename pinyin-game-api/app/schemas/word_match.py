"""词语连连看 Schema。"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List, Optional


class WordBookOut(BaseModel):
    id: int
    title: str
    description: str
    question_count: int
    status: int

    class Config:
        from_attributes = True


class WordBookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=128)
    description: str = ""
    status: int = 1


class WordBookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None


class WordQuestionOut(BaseModel):
    id: int
    book_id: int
    word: str
    pinyin: str
    word_len: int
    meaning: Optional[str] = None
    sort_order: int
    audio_url: Optional[str] = None

    class Config:
        from_attributes = True


class WordQuestionCreate(BaseModel):
    word: str = Field(..., min_length=2, max_length=4)
    meaning: Optional[str] = None
    sort_order: int = 0


class WordQuestionUpdate(BaseModel):
    word: Optional[str] = None
    meaning: Optional[str] = None
    sort_order: Optional[int] = None


class WordQuestionBatchImport(BaseModel):
    text: str = Field(..., description="每行一个词语，2～4 字")


class WordMetaOut(BaseModel):
    """本轮出现的词语元信息（整词朗读用）。"""

    question_id: int
    word: str
    word_len: int
    audio_url: Optional[str] = None


class WordCharCardOut(BaseModel):
    """单字卡片。"""

    card_id: str
    question_id: int
    char_index: int
    text: str
    pinyin: str = ""
    audio_url: Optional[str] = None


class WordMatchGameDataOut(BaseModel):
    book_id: int
    book_title: str
    total: int
    total_cards: int
    words: List[WordMetaOut]
    cards: List[WordCharCardOut]


class WordMatchAnswerItem(BaseModel):
    question_id: int


class WordMatchSubmitRequest(BaseModel):
    book_id: int
    answers: List[WordMatchAnswerItem]
    duration_seconds: int = 0


class WordMatchWrongAttemptRequest(BaseModel):
    book_id: int
    question_id: int
