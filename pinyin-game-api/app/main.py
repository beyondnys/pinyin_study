"""FastAPI 应用入口。"""

from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth
from app.routers.admin import books as admin_books
from app.routers.admin import dashboard as admin_dashboard
from app.routers.admin import import_tasks as admin_import
from app.routers.admin import practice_records as admin_records
from app.routers.admin import users as admin_users
from app.routers.admin import tts as admin_tts
from app.routers.admin import words as admin_words
from app.routers.admin import word_books as admin_word_books
from app.routers.admin import word_match_records as admin_word_match_records
from app.routers.web import books as web_books
from app.routers.web import practice as web_practice
from app.routers.web import wrong_questions as web_wrong
from app.routers.admin import wrong_questions as admin_wrong
from app.routers.web import word_books as web_word_books
from app.routers.web import word_match as web_word_match
from app.routers.game import pinyin_select as game_pinyin_select

app = FastAPI(title="拼音练习 API", version="1.0.0")

_origins = ["*"] if settings.CORS_ORIGINS == "*" else [o.strip() for o in settings.CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(admin_dashboard.router, prefix="/api/admin/dashboard", tags=["管理-仪表盘"])
app.include_router(admin_users.router, prefix="/api/admin/users", tags=["管理-用户"])
app.include_router(admin_words.router, prefix="/api/admin/words", tags=["管理-字库"])
app.include_router(admin_tts.router, prefix="/api/admin/tts", tags=["管理-TTS"])
app.include_router(admin_books.router, prefix="/api/admin/books", tags=["管理-练习册"])
app.include_router(admin_word_books.router, prefix="/api/admin/word-books", tags=["管理-词语词库"])
app.include_router(admin_import.router, prefix="/api/admin/import-tasks", tags=["管理-导入"])
app.include_router(admin_records.router, prefix="/api/admin/practice-records", tags=["管理-拼音学习记录"])
app.include_router(
    admin_word_match_records.router,
    prefix="/api/admin/word-match-records",
    tags=["管理-词语学习记录"],
)
app.include_router(admin_wrong.router, prefix="/api/admin/wrong-questions", tags=["管理-错题"])
app.include_router(web_books.router, prefix="/api/web/books", tags=["前台-练习册"])
app.include_router(web_word_books.router, prefix="/api/web/word-books", tags=["前台-词语词库"])
app.include_router(web_word_match.router, prefix="/api/web/word-match", tags=["前台-词语连连看"])
app.include_router(web_practice.router, prefix="/api/web/practice", tags=["前台-练习"])
app.include_router(web_wrong.router, prefix="/api/web/wrong-questions", tags=["前台-错题"])
app.include_router(
    game_pinyin_select.router,
    prefix="/api/game/pinyin-select",
    tags=["游戏-拼音练习"],
)


@app.get("/api/health")
def health():
    """健康检查。"""
    return {"status": "ok"}
