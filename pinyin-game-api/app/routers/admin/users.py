"""用户管理。"""

from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.user import User
from app.response import fail, success
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.utils.password_util import hash_password

router = APIRouter(dependencies=[Depends(require_admin)])


@router.get("")
def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """分页用户列表。"""
    q = db.query(User).filter(User.is_deleted == 0)
    total = q.count()
    items = q.order_by(User.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return success({"total": total, "items": [UserOut.model_validate(u).model_dump() for u in items]})


@router.post("")
def create_user(body: UserCreate, db: Session = Depends(get_db), admin: dict = Depends(require_admin)):
    """创建用户。"""
    if db.query(User).filter(User.username == body.username, User.is_deleted == 0).first():
        return fail(1, "用户名已存在")
    u = User(
        username=body.username,
        password_hash=hash_password(body.password),
        nickname=body.nickname,
        role=body.role,
        status=body.status,
        created_by=admin["user_id"],
        updated_by=admin["user_id"],
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return success(UserOut.model_validate(u).model_dump())


@router.put("/{user_id}")
def update_user(user_id: int, body: UserUpdate, db: Session = Depends(get_db), admin: dict = Depends(require_admin)):
    """更新用户。"""
    u = db.query(User).filter(User.id == user_id, User.is_deleted == 0).first()
    if not u:
        return fail(1, "用户不存在")
    if body.nickname is not None:
        u.nickname = body.nickname
    if body.role is not None:
        u.role = body.role
    if body.status is not None:
        u.status = body.status
    if body.password:
        u.password_hash = hash_password(body.password)
    u.updated_by = admin["user_id"]
    db.commit()
    return success(UserOut.model_validate(u).model_dump())


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), admin: dict = Depends(require_admin)):
    """软删除用户。"""
    u = db.query(User).filter(User.id == user_id, User.is_deleted == 0).first()
    if not u:
        return fail(1, "用户不存在")
    u.is_deleted = 1
    u.updated_by = admin["user_id"]
    db.commit()
    return success()
