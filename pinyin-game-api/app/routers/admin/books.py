"""练习册管理。"""

from __future__ import annotations
from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.practice_book import PracticeBook
from app.models.practice_question import PracticeQuestion
from app.response import fail, success
from app.schemas.book import BookCreate, BookOut, BookUpdate
from app.schemas.question import (
    QuestionBatchImport,
    QuestionCreate,
    QuestionOut,
    QuestionUpdate,
)
from app.services.pinyin_service import hanzi_to_pinyin
from app.utils.pinyin_util import apply_pinyin_fields, question_to_out_dict
from app.services.question_import_service import batch_import_book_questions
from app.services.tts.tts_audio_service import (
    generate_tts_for_question,
    lookup_question_audio_map,
    run_tts_background_for_questions,
)

router = APIRouter(dependencies=[Depends(require_admin)])


@router.get("")
def list_books(page: int = 1, page_size: int = 20, db: Session = Depends(get_db)):
    """练习册列表。"""
    q = db.query(PracticeBook).filter(PracticeBook.is_deleted == 0)
    total = q.count()
    items = q.order_by(PracticeBook.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return success({"total": total, "items": [BookOut.model_validate(b).model_dump() for b in items]})


@router.post("")
def create_book(body: BookCreate, db: Session = Depends(get_db), admin: dict = Depends(require_admin)):
    """创建练习册。"""
    b = PracticeBook(
        title=body.title,
        description=body.description,
        status=body.status,
        created_by=admin["user_id"],
        updated_by=admin["user_id"],
    )
    db.add(b)
    db.commit()
    db.refresh(b)
    return success(BookOut.model_validate(b).model_dump())


@router.put("/{book_id}")
def update_book(book_id: int, body: BookUpdate, db: Session = Depends(get_db), admin: dict = Depends(require_admin)):
    """更新练习册。"""
    b = db.query(PracticeBook).filter(PracticeBook.id == book_id, PracticeBook.is_deleted == 0).first()
    if not b:
        return fail(1, "练习册不存在")
    if body.title is not None:
        b.title = body.title
    if body.description is not None:
        b.description = body.description
    if body.status is not None:
        b.status = body.status
    b.updated_by = admin["user_id"]
    db.commit()
    return success(BookOut.model_validate(b).model_dump())


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), admin: dict = Depends(require_admin)):
    """软删除练习册。"""
    b = db.query(PracticeBook).filter(PracticeBook.id == book_id, PracticeBook.is_deleted == 0).first()
    if not b:
        return fail(1, "练习册不存在")
    b.is_deleted = 1
    b.updated_by = admin["user_id"]
    db.commit()
    return success()


@router.get("/{book_id}/questions")
def list_questions(book_id: int, db: Session = Depends(get_db)):
    """练习册题目列表。"""
    items = (
        db.query(PracticeQuestion)
        .filter(PracticeQuestion.book_id == book_id, PracticeQuestion.is_deleted == 0)
        .order_by(PracticeQuestion.sort_order, PracticeQuestion.id)
        .all()
    )
    qids = [q.id for q in items]
    audio_map = lookup_question_audio_map(db, qids)
    return success([question_to_out_dict(q, audio_map.get(q.id)) for q in items])


@router.post("/{book_id}/questions/batch-import")
async def batch_import_questions(
    book_id: int,
    body: QuestionBatchImport,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin),
):
    """
    批量文本导入题目：去无效字符；跳过本册已有、字库已有汉字。
    """
    try:
        result = batch_import_book_questions(db, book_id, body.raw_text, admin["user_id"])
    except ValueError as e:
        return fail(1, str(e))
    if result["added_count"] == 0 and not result["skipped_in_book"] and not result["skipped_in_library"]:
        return fail(1, "未识别到可导入的汉字")
    qids = result.get("added_question_ids") or []
    if qids:
        background_tasks.add_task(
            run_tts_background_for_questions,
            qids,
            admin.get("user_id"),
        )
    return success(result)


@router.post("/{book_id}/questions")
async def create_question(
    book_id: int, body: QuestionCreate, db: Session = Depends(get_db), admin: dict = Depends(require_admin)
):
    """为练习册添加题目。"""
    b = db.query(PracticeBook).filter(PracticeBook.id == book_id, PracticeBook.is_deleted == 0).first()
    if not b:
        return fail(1, "练习册不存在")
    py_result = hanzi_to_pinyin(body.hanzi)
    q = PracticeQuestion(
        book_id=book_id,
        hanzi=body.hanzi,
        pinyin="",
        pinyin_list="[]",
        sort_order=body.sort_order,
        created_by=admin["user_id"],
        updated_by=admin["user_id"],
    )
    apply_pinyin_fields(q, py_result, manual_pinyin=body.pinyin)
    db.add(q)
    b.question_count = (
        db.query(PracticeQuestion)
        .filter(PracticeQuestion.book_id == book_id, PracticeQuestion.is_deleted == 0)
        .count()
        + 1
    )
    db.commit()
    db.refresh(q)
    await generate_tts_for_question(db, q.id, q.hanzi, q.pinyin, admin.get("user_id"))
    audio = lookup_question_audio_map(db, [q.id]).get(q.id)
    return success(question_to_out_dict(q, audio))


@router.put("/{book_id}/questions/{question_id}")
def update_question(
    book_id: int,
    question_id: int,
    body: QuestionUpdate,
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin),
):
    """更新题目。"""
    q = (
        db.query(PracticeQuestion)
        .filter(
            PracticeQuestion.id == question_id,
            PracticeQuestion.book_id == book_id,
            PracticeQuestion.is_deleted == 0,
        )
        .first()
    )
    if not q:
        return fail(1, "题目不存在")
    if body.hanzi is not None:
        q.hanzi = body.hanzi
    if body.hanzi is not None or body.pinyin is not None:
        py_result = hanzi_to_pinyin(q.hanzi)
        apply_pinyin_fields(q, py_result, manual_pinyin=body.pinyin)
    if body.sort_order is not None:
        q.sort_order = body.sort_order
    q.updated_by = admin["user_id"]
    db.commit()
    audio = lookup_question_audio_map(db, [q.id]).get(q.id)
    return success(question_to_out_dict(q, audio))


@router.delete("/{book_id}/questions/{question_id}")
def delete_question(
    book_id: int, question_id: int, db: Session = Depends(get_db), admin: dict = Depends(require_admin)
):
    """软删除题目。"""
    q = (
        db.query(PracticeQuestion)
        .filter(
            PracticeQuestion.id == question_id,
            PracticeQuestion.book_id == book_id,
            PracticeQuestion.is_deleted == 0,
        )
        .first()
    )
    if not q:
        return fail(1, "题目不存在")
    q.is_deleted = 1
    q.updated_by = admin["user_id"]
    b = db.query(PracticeBook).filter(PracticeBook.id == book_id).first()
    if b:
        b.question_count = max(
            0,
            db.query(PracticeQuestion)
            .filter(PracticeQuestion.book_id == book_id, PracticeQuestion.is_deleted == 0)
            .count()
            - 1,
        )
    db.commit()
    return success()
