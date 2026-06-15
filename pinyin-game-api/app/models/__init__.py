"""导出所有 ORM 模型，便于 Alembic 与建表。"""

from __future__ import annotations
from app.models.user import User
from app.models.word_library import WordLibrary
from app.models.practice_book import PracticeBook
from app.models.practice_question import PracticeQuestion
from app.models.practice_record import PracticeRecord
from app.models.practice_answer_detail import PracticeAnswerDetail
from app.models.wrong_question import WrongQuestion
from app.models.user_item_mastery import UserItemMastery
from app.models.import_task import ImportTask
from app.models.pinyin_question import PinyinQuestion
from app.models.pinyin_game_record import PinyinGameRecord
from app.models.word_book import WordBook
from app.models.word_question import WordQuestion
from app.models.word_match_record import WordMatchRecord
from app.models.word_match_answer_detail import WordMatchAnswerDetail

__all__ = [
    "User",
    "WordLibrary",
    "PracticeBook",
    "PracticeQuestion",
    "PracticeRecord",
    "PracticeAnswerDetail",
    "WrongQuestion",
    "UserItemMastery",
    "ImportTask",
    "PinyinQuestion",
    "PinyinGameRecord",
    "WordBook",
    "WordQuestion",
    "WordMatchRecord",
    "WordMatchAnswerDetail",
]
