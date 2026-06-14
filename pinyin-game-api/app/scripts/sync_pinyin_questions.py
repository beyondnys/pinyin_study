"""
从练习册题目、字库同步单字到 pinyin_question。

用法（在 pinyin-game-api 目录）：
    mysql ... < ../sql/migrate_pinyin_select_game.sql
    python -m app.scripts.sync_pinyin_questions
    python -m app.scripts.sync_pinyin_questions --dry-run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.database import SessionLocal
from app.models.pinyin_question import PinyinQuestion
from app.models.practice_question import PracticeQuestion
from app.models.word_library import WordLibrary
from app.services.pinyin_service import is_hanzi
from app.utils.pinyin_split_util import hanzi_to_components


def _upsert_question(
    db,
    hanzi: str,
    source_type: str,
    source_id: int,
    dry_run: bool,
) -> str:
    """返回 created | updated | skip。"""
    if len(hanzi) != 1 or not is_hanzi(hanzi):
        return "skip"
    try:
        initial, final, tone, display = hanzi_to_components(hanzi)
    except ValueError:
        return "skip"

    row = (
        db.query(PinyinQuestion)
        .filter(PinyinQuestion.hanzi == hanzi, PinyinQuestion.is_deleted == 0)
        .first()
    )
    if dry_run:
        action = "update" if row else "create"
        print(f"  [{action}] {hanzi} -> {display} ({initial}|{final}|{tone})")
        return action

    if row:
        row.initial = initial
        row.final = final
        row.tone = tone
        row.pinyin_display = display
        row.source_type = source_type
        row.source_id = source_id
        row.status = 1
        return "updated"

    db.add(
        PinyinQuestion(
            hanzi=hanzi,
            initial=initial,
            final=final,
            tone=tone,
            pinyin_display=display,
            source_type=source_type,
            source_id=source_id,
            status=1,
        )
    )
    return "created"


def main() -> None:
    parser = argparse.ArgumentParser(description="同步拼音练习游戏题库")
    parser.add_argument("--dry-run", action="store_true", help="仅预览")
    args = parser.parse_args()

    db = SessionLocal()
    stats = {"created": 0, "updated": 0, "skip": 0}
    seen: set[str] = set()

    try:
        for q in db.query(PracticeQuestion).filter(PracticeQuestion.is_deleted == 0).all():
            if q.hanzi in seen:
                continue
            seen.add(q.hanzi)
            action = _upsert_question(db, q.hanzi, "practice_question", q.id, args.dry_run)
            stats[action if action in stats else "skip"] += 1

        for w in db.query(WordLibrary).filter(WordLibrary.is_deleted == 0).all():
            if w.hanzi in seen:
                continue
            seen.add(w.hanzi)
            action = _upsert_question(db, w.hanzi, "word_library", w.id, args.dry_run)
            stats[action if action in stats else "skip"] += 1

        if not args.dry_run:
            db.commit()
        print(
            f"完成：新增 {stats['created']}，更新 {stats['updated']}，"
            f"跳过 {stats['skip']}，去重汉字 {len(seen)} 个。"
        )
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
