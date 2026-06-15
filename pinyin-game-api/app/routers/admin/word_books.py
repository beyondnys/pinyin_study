"""词语词库管理。"""

from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.word_book import WordBook
from app.models.word_question import WordQuestion
from app.response import fail, success
from app.schemas.word_match import (
    WordBookCreate,
    WordBookOut,
    WordBookUpdate,
    WordQuestionBatchImport,
    WordQuestionCreate,
    WordQuestionOut,
    WordQuestionUpdate,
)
from app.services.tts.tts_audio_service import (
    lookup_word_match_audio_map,
    run_tts_background_for_word_questions_sync,
)
from app.services.word_match_service import (
    apply_pinyin_to_word_question,
    batch_import_word_questions,
    create_word_question,
)
from app.utils.word_split_util import validate_word

router = APIRouter(dependencies=[Depends(require_admin)])


@router.get("")
def list_books(page: int = 1, page_size: int = 20, db: Session = Depends(get_db)):
    """词语词库列表。"""
    q = db.query(WordBook).filter(WordBook.is_deleted == 0)
    total = q.count()
    items = q.order_by(WordBook.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return success({"total": total, "items": [WordBookOut.model_validate(b).model_dump() for b in items]})


@router.post("")
def create_book(body: WordBookCreate, db: Session = Depends(get_db), admin: dict = Depends(require_admin)):
    """创建词语词库。"""
    b = WordBook(
        title=body.title,
        description=body.description,
        status=body.status,
        created_by=admin["user_id"],
        updated_by=admin["user_id"],
    )
    db.add(b)
    db.commit()
    db.refresh(b)
    return success(WordBookOut.model_validate(b).model_dump())


@router.put("/{book_id}")
def update_book(book_id: int, body: WordBookUpdate, db: Session = Depends(get_db), admin: dict = Depends(require_admin)):
    """更新词语词库。"""
    b = db.query(WordBook).filter(WordBook.id == book_id, WordBook.is_deleted == 0).first()
    if not b:
        return fail(1, "词库不存在")
    if body.title is not None:
        b.title = body.title
    if body.description is not None:
        b.description = body.description
    if body.status is not None:
        b.status = body.status
    b.updated_by = admin["user_id"]
    db.commit()
    return success(WordBookOut.model_validate(b).model_dump())


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), admin: dict = Depends(require_admin)):
    """软删除词语词库。"""
    b = db.query(WordBook).filter(WordBook.id == book_id, WordBook.is_deleted == 0).first()
    if not b:
        return fail(1, "词库不存在")
    b.is_deleted = 1
    b.updated_by = admin["user_id"]
    db.commit()
    return success()


@router.get("/{book_id}/questions")
def list_questions(book_id: int, db: Session = Depends(get_db)):
    """词库题目列表。"""
    items = (
        db.query(WordQuestion)
        .filter(WordQuestion.book_id == book_id, WordQuestion.is_deleted == 0)
        .order_by(WordQuestion.sort_order, WordQuestion.id)
        .all()
    )
    qids = [q.id for q in items]
    audio_map = lookup_word_match_audio_map(db, qids)
    out = []
    for q in items:
        row = WordQuestionOut.model_validate(q).model_dump()
        row["audio_url"] = audio_map.get(q.id)
        out.append(row)
    return success(out)


def _submit_word_questions_tts_task(
    db: Session,
    book_id: int,
    background_tasks: BackgroundTasks,
    admin: dict,
) -> dict:
    """为词库内全部词语提交后台 TTS 任务（整词 + 单字）。"""
    book = db.query(WordBook).filter(WordBook.id == book_id, WordBook.is_deleted == 0).first()
    if not book:
        raise ValueError("词库不存在")

    qids = [
        q.id
        for q in db.query(WordQuestion)
        .filter(WordQuestion.book_id == book_id, WordQuestion.is_deleted == 0)
        .all()
    ]
    if not qids:
        raise ValueError("该词库暂无词语")

    background_tasks.add_task(run_tts_background_for_word_questions_sync, qids, admin["user_id"])
    return {
        "count": len(qids),
        "message": f"已为 {len(qids)} 个词语提交读音生成任务，请稍后刷新列表",
    }


@router.post("/{book_id}/questions/batch-import")
async def batch_import(
    book_id: int,
    body: WordQuestionBatchImport,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin),
):
    """批量导入词语，每行一个 2～4 字词（单次事务，读音后台异步生成）。"""
    try:
        result = batch_import_word_questions(db, book_id, body.text, admin["user_id"])
    except ValueError as e:
        return fail(1, str(e))

    created_ids = result.get("created_ids") or []
    if created_ids:
        background_tasks.add_task(
            run_tts_background_for_word_questions_sync,
            created_ids,
            admin["user_id"],
        )

    return success(
        {
            "created": result["created"],
            "errors": result["errors"],
            "skipped": result.get("skipped") or [],
            "tts_pending": len(created_ids),
            "message": "导入完成，整词与单字读音正在后台生成，请稍后刷新列表"
            if created_ids
            else None,
        }
    )


@router.post("/{book_id}/retry-word-tts")
@router.post("/{book_id}/questions/retry-tts")
async def retry_word_questions_tts(
    book_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin),
):
    """为词库内全部词语重新触发 TTS 生成（整词 + 单字）。"""
    try:
        payload = _submit_word_questions_tts_task(db, book_id, background_tasks, admin)
    except ValueError as e:
        return fail(1, str(e))
    return success(payload)


@router.post("/{book_id}/questions")
async def create_question(
    book_id: int,
    body: WordQuestionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin),
):
    """新增词语题目。"""
    try:
        q = create_word_question(
            db,
            book_id,
            body.word,
            meaning=body.meaning,
            sort_order=body.sort_order,
            operator_id=admin["user_id"],
        )
    except ValueError as e:
        return fail(1, str(e))
    background_tasks.add_task(run_tts_background_for_word_questions_sync, [q.id], admin["user_id"])
    return success(WordQuestionOut.model_validate(q).model_dump())


@router.put("/{book_id}/questions/{question_id:int}")
async def update_question(
    book_id: int,
    question_id: int,
    body: WordQuestionUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin),
):
    """更新词语题目。"""
    q = (
        db.query(WordQuestion)
        .filter(
            WordQuestion.id == question_id,
            WordQuestion.book_id == book_id,
            WordQuestion.is_deleted == 0,
        )
        .first()
    )
    if not q:
        return fail(1, "题目不存在")
    word_changed = False
    if body.word is not None:
        try:
            validated = validate_word(body.word)
        except ValueError as e:
            return fail(1, str(e))
        q.word = validated
        q.word_len = len(validated)
        apply_pinyin_to_word_question(q)
        word_changed = True
    if body.meaning is not None:
        q.meaning = body.meaning
    if body.sort_order is not None:
        q.sort_order = body.sort_order
    q.updated_by = admin["user_id"]
    db.commit()
    if word_changed:
        background_tasks.add_task(run_tts_background_for_word_questions_sync, [q.id], admin["user_id"])
    return success(WordQuestionOut.model_validate(q).model_dump())


@router.delete("/{book_id}/questions/{question_id:int}")
def delete_question(
    book_id: int,
    question_id: int,
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin),
):
    """软删除词语题目。"""
    q = (
        db.query(WordQuestion)
        .filter(
            WordQuestion.id == question_id,
            WordQuestion.book_id == book_id,
            WordQuestion.is_deleted == 0,
        )
        .first()
    )
    if not q:
        return fail(1, "题目不存在")
    q.is_deleted = 1
    q.updated_by = admin["user_id"]
    book = db.query(WordBook).filter(WordBook.id == book_id).first()
    if book:
        book.question_count = max(
            0,
            db.query(WordQuestion)
            .filter(WordQuestion.book_id == book_id, WordQuestion.is_deleted == 0)
            .count(),
        )
    db.commit()
    return success()
