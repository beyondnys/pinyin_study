"""导入任务 Schema。"""

from __future__ import annotations
from pydantic import BaseModel
from typing import Optional


class ImportTaskCreate(BaseModel):
    title: str
    raw_text: str
    book_title: Optional[str] = None  # 新建练习册标题，为空则用 title


class ImportTaskOut(BaseModel):
    id: int
    title: str
    book_id: Optional[int]
    status: str
    result_message: str

    class Config:
        from_attributes = True
