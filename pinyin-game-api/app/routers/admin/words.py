"""字库管理。"""

from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.word_library import WordLibrary
from app.response import fail, success
from app.schemas.word import WordCreate, WordOut, WordUpdate
from app.services.pinyin_service import hanzi_to_pinyin

router = APIRouter(dependencies=[Depends(require_admin)])


@router.get("")
def list_words(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: str = "",
    db: Session = Depends(get_db),
):
    """分页字库列表。"""
    q = db.query(WordLibrary).filter(WordLibrary.is_deleted == 0)
    if keyword:
        q = q.filter(WordLibrary.hanzi.contains(keyword))
    total = q.count()
    items = q.order_by(WordLibrary.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return success({"total": total, "items": [WordOut.model_validate(w).model_dump() for w in items]})


@router.post("")
def create_word(body: WordCreate, db: Session = Depends(get_db), admin: dict = Depends(require_admin)):
    """新增字库条目，拼音可自动生成。"""
    py, plain = hanzi_to_pinyin(body.hanzi)
    pinyin = body.pinyin or py
    w = WordLibrary(
        hanzi=body.hanzi,
        pinyin=pinyin,
        pinyin_plain=plain,
        remark=body.remark,
        created_by=admin["user_id"],
        updated_by=admin["user_id"],
    )
    db.add(w)
    db.commit()
    db.refresh(w)
    return success(WordOut.model_validate(w).model_dump())


@router.put("/{word_id}")
def update_word(word_id: int, body: WordUpdate, db: Session = Depends(get_db), admin: dict = Depends(require_admin)):
    """更新字库。"""
    w = db.query(WordLibrary).filter(WordLibrary.id == word_id, WordLibrary.is_deleted == 0).first()
    if not w:
        return fail(1, "记录不存在")
    if body.hanzi is not None:
        w.hanzi = body.hanzi
    if body.pinyin is not None:
        w.pinyin = body.pinyin
        _, plain = hanzi_to_pinyin(w.hanzi)
        w.pinyin_plain = plain
    if body.remark is not None:
        w.remark = body.remark
    w.updated_by = admin["user_id"]
    db.commit()
    return success(WordOut.model_validate(w).model_dump())


@router.delete("/{word_id}")
def delete_word(word_id: int, db: Session = Depends(get_db), admin: dict = Depends(require_admin)):
    """软删除字库。"""
    w = db.query(WordLibrary).filter(WordLibrary.id == word_id, WordLibrary.is_deleted == 0).first()
    if not w:
        return fail(1, "记录不存在")
    w.is_deleted = 1
    w.updated_by = admin["user_id"]
    db.commit()
    return success()
