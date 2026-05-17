"""认证路由。"""

from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.response import fail, success
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest, UserInfo
from app.services import auth_service

router = APIRouter()


@router.post("/register")
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    """学生自助注册，成功后自动登录并返回 Token。"""
    try:
        user = auth_service.register_student(
            db, body.username, body.password, body.nickname
        )
        token, user = auth_service.login(db, user.username, body.password)
    except ValueError as e:
        return fail(1, str(e))
    data = LoginResponse(
        token=token,
        user_id=user.id,
        username=user.username,
        nickname=user.nickname,
        role=user.role,
    )
    return success(data.model_dump())


@router.post("/login")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    """用户登录，返回 JWT Token。"""
    try:
        token, user = auth_service.login(db, body.username, body.password)
    except ValueError as e:
        return fail(1, str(e))
    data = LoginResponse(
        token=token,
        user_id=user.id,
        username=user.username,
        nickname=user.nickname,
        role=user.role,
    )
    return success(data.model_dump())


@router.post("/logout")
def logout(user: dict = Depends(get_current_user)):
    """退出登录，清除 Redis Token。"""
    auth_service.logout(user["token"], user["user_id"])
    return success()


@router.get("/me")
def me(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取当前登录用户信息。"""
    from app.models.user import User

    u = db.query(User).filter(User.id == user["user_id"], User.is_deleted == 0).first()
    if not u:
        return fail(1, "用户不存在")
    info = UserInfo(user_id=u.id, username=u.username, nickname=u.nickname, role=u.role)
    return success(info.model_dump())
