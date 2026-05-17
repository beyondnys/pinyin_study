"""文本导入任务管理。"""

from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.import_task import ImportTask
from app.response import success
from app.schemas.import_task import ImportTaskCreate, ImportTaskOut
from app.services.import_service import process_import_task

router = APIRouter(dependencies=[Depends(require_admin)])


@router.get("")
def list_tasks(page: int = 1, page_size: int = 20, db: Session = Depends(get_db)):
    """导入任务列表。"""
    q = db.query(ImportTask).filter(ImportTask.is_deleted == 0)
    total = q.count()
    items = q.order_by(ImportTask.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return success({"total": total, "items": [ImportTaskOut.model_validate(t).model_dump() for t in items]})


@router.post("")
def create_task(body: ImportTaskCreate, db: Session = Depends(get_db), admin: dict = Depends(require_admin)):
    """创建并同步执行导入任务。"""
    task = ImportTask(
        title=body.title,
        raw_text=body.raw_text,
        status="pending",
        created_by=admin["user_id"],
        updated_by=admin["user_id"],
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    task = process_import_task(db, task, body.book_title, admin["user_id"])
    return success(ImportTaskOut.model_validate(task).model_dump())


@router.get("/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    """导入任务详情。"""
    task = db.query(ImportTask).filter(ImportTask.id == task_id, ImportTask.is_deleted == 0).first()
    if not task:
        from app.response import fail

        return fail(1, "任务不存在")
    return success(ImportTaskOut.model_validate(task).model_dump())
