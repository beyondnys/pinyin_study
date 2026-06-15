"""词语连连看演示词库种子（可选）。"""

from __future__ import annotations

import argparse

from app.database import SessionLocal
from app.models.word_book import WordBook
from app.models.word_question import WordQuestion
from app.services.word_match_service import create_word_question

DEMO_WORDS = [
    "中国",
    "北京",
    "飞机",
    "太阳",
    "月亮",
    "学校",
    "自行车",
    "计算机",
    "春暖花开",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="创建词语连连看演示词库")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        book = (
            db.query(WordBook)
            .filter(WordBook.title == "演示词语", WordBook.is_deleted == 0)
            .first()
        )
        if not book:
            if args.dry_run:
                print(f"将创建词库「演示词语」，词语 {len(DEMO_WORDS)} 个")
                return
            book = WordBook(title="演示词语", description="词语连连看演示", status=1)
            db.add(book)
            db.flush()

        for w in DEMO_WORDS:
            exists = (
                db.query(WordQuestion)
                .filter(
                    WordQuestion.book_id == book.id,
                    WordQuestion.word == w,
                    WordQuestion.is_deleted == 0,
                )
                .first()
            )
            if exists:
                continue
            if args.dry_run:
                print(f"  + {w}")
                continue
            create_word_question(db, book.id, w)

        if not args.dry_run:
            db.commit()
            print(f"演示词库 id={book.id}，词语数 {book.question_count}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
