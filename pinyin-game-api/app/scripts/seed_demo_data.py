"""填充演示数据：学生账号、字库、练习册与题目（约 10 字，适合 4x4 宫格）。"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.database import SessionLocal
from app.models.practice_book import PracticeBook
from app.models.practice_question import PracticeQuestion
from app.models.user import User
from app.models.word_library import WordLibrary
from app.services.pinyin_service import hanzi_to_pinyin
from app.utils.password_util import hash_password
from app.utils.pinyin_util import apply_pinyin_fields

# 与参考图类似的常用字
DEMO_HANZI = ["山", "水", "田", "风", "云", "花", "雨", "禾", "石", "对"]
BOOK_TITLE = "拼音练习册（一年级）"


def main():
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "student", User.is_deleted == 0).first():
            db.add(
                User(
                    username="student",
                    password_hash=hash_password("student123"),
                    nickname="小明",
                    role="student",
                    status=1,
                )
            )
            print("已创建学生：student / student123")

        for hz in DEMO_HANZI:
            word = db.query(WordLibrary).filter(WordLibrary.hanzi == hz, WordLibrary.is_deleted == 0).first()
            py_result = hanzi_to_pinyin(hz)
            if not word:
                word = WordLibrary(
                    hanzi=hz,
                    pinyin="",
                    pinyin_list="[]",
                    pinyin_plain="",
                    remark="演示",
                )
                apply_pinyin_fields(word, py_result)
                db.add(word)
            else:
                apply_pinyin_fields(word, py_result)

        book = db.query(PracticeBook).filter(PracticeBook.title == BOOK_TITLE, PracticeBook.is_deleted == 0).first()
        if not book:
            book = PracticeBook(
                title=BOOK_TITLE,
                description="山山水田风云花雨禾石对，点击进入后每次随机 8 题",
                question_count=0,
                status=1,
            )
            db.add(book)
            db.flush()

        existing = {
            q.hanzi
            for q in db.query(PracticeQuestion)
            .filter(PracticeQuestion.book_id == book.id, PracticeQuestion.is_deleted == 0)
            .all()
        }
        sort_order = len(existing)
        for hz in DEMO_HANZI:
            if hz in existing:
                continue
            py_result = hanzi_to_pinyin(hz)
            q = PracticeQuestion(
                book_id=book.id,
                hanzi=hz,
                pinyin="",
                pinyin_list="[]",
                sort_order=sort_order,
            )
            apply_pinyin_fields(q, py_result)
            db.add(q)
            sort_order += 1

        book.question_count = (
            db.query(PracticeQuestion)
            .filter(PracticeQuestion.book_id == book.id, PracticeQuestion.is_deleted == 0)
            .count()
        )
        db.commit()
        print(f"练习册「{book.title}」共 {book.question_count} 题")
        print("演示数据填充完成。前台可进入练习册开始练习。")
    finally:
        db.close()


if __name__ == "__main__":
    main()
