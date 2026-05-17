"""文本导入任务模型。"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import BigInteger, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import AuditMixin


class ImportTask(Base, AuditMixin):
    """文本导入任务表 import_tasks，用于批量生成练习册题目。"""

    __tablename__ = "import_tasks"

    title: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        comment="任务名称",
    )
    raw_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="待导入的原始文本内容",
    )
    book_id: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        nullable=True,
        comment="目标练习册 ID，未指定时为空",
    )
    status: Mapped[str] = mapped_column(
        Enum("pending", "processing", "done", "failed", name="import_status"),
        default="pending",
        comment="任务状态：pending / processing / done / failed",
    )
    result_message: Mapped[str] = mapped_column(
        String(512),
        default="",
        nullable=False,
        comment="执行结果说明，成功条数或失败原因",
    )
