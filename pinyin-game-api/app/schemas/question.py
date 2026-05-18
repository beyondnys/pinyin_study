"""题目 Schema。"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class QuestionCreate(BaseModel):
    hanzi: str
    pinyin: Optional[str] = None
    sort_order: int = 0


class QuestionUpdate(BaseModel):
    hanzi: Optional[str] = None
    pinyin: Optional[str] = None
    sort_order: Optional[int] = None


class QuestionOut(BaseModel):
    id: int
    book_id: int
    hanzi: str
    pinyin: str
    pinyin_list: List[str] = []
    sort_order: int

    class Config:
        from_attributes = True


class QuestionBatchImport(BaseModel):
    """练习册题目批量文本导入。"""

    raw_text: str = Field(..., min_length=1, description="粘贴的课文或字表文本")


class QuestionBatchImportResult(BaseModel):
    """批量导入结果摘要。"""

    added_count: int
    added_hanzi: List[str]
    skipped_in_book: List[str]
    skipped_in_library: List[str]
    invalid_stripped: int
