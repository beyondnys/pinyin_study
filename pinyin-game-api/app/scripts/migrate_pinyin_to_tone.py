"""
将字库、题目等拼音从数字调迁移为声调符号，并填充多音字列表。

用法（在 pinyin-game-api 目录下）：
    # 先执行 SQL：mysql ... pinyin_game < ../sql/migrate_pinyin_tone.sql
    python -m app.scripts.migrate_pinyin_to_tone
    python -m app.scripts.migrate_pinyin_to_tone --dry-run   # 仅预览不写库
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.database import SessionLocal
from app.models.practice_answer_detail import PracticeAnswerDetail
from app.models.practice_question import PracticeQuestion
from app.models.word_library import WordLibrary
from app.models.wrong_question import WrongQuestion
from app.services.pinyin_service import hanzi_to_pinyin
from app.utils.pinyin_util import apply_pinyin_fields


def _migrate_words(db, dry_run: bool) -> int:
    rows = db.query(WordLibrary).filter(WordLibrary.is_deleted == 0).all()
    n = 0
    for w in rows:
        result = hanzi_to_pinyin(w.hanzi)
        if dry_run:
            print(f"  [字库] {w.hanzi}: {w.pinyin} -> {result.pinyin}  多音: {result.pinyin_list}")
        else:
            apply_pinyin_fields(w, result)
        n += 1
    return n


def _migrate_questions(db, dry_run: bool) -> int:
    rows = db.query(PracticeQuestion).filter(PracticeQuestion.is_deleted == 0).all()
    n = 0
    for q in rows:
        result = hanzi_to_pinyin(q.hanzi)
        if dry_run:
            print(f"  [题目] {q.hanzi}: {q.pinyin} -> {result.pinyin}  多音: {result.pinyin_list}")
        else:
            apply_pinyin_fields(q, result)
        n += 1
    return n


def _migrate_wrong(db, dry_run: bool) -> int:
    """错题本仅更新展示用拼音，按汉字重算。"""
    rows = db.query(WrongQuestion).filter(WrongQuestion.is_deleted == 0).all()
    n = 0
    for row in rows:
        result = hanzi_to_pinyin(row.hanzi)
        if dry_run:
            print(f"  [错题] {row.hanzi}: {row.pinyin} -> {result.pinyin}")
        else:
            row.pinyin = result.pinyin
        n += 1
    return n


def _migrate_answer_details(db, dry_run: bool) -> int:
    """历史作答详情中的标准音同步为新格式（按汉字重算主音）。"""
    rows = db.query(PracticeAnswerDetail).filter(PracticeAnswerDetail.is_deleted == 0).all()
    n = 0
    for d in rows:
        if not d.hanzi:
            continue
        result = hanzi_to_pinyin(d.hanzi)
        if dry_run:
            if d.correct_pinyin != result.pinyin:
                print(f"  [作答] {d.hanzi}: {d.correct_pinyin} -> {result.pinyin}")
        else:
            d.correct_pinyin = result.pinyin
        n += 1
    return n


def run_migration(dry_run: bool = False) -> None:
    db = SessionLocal()
    try:
        print("开始迁移拼音（声调符号 + 多音字列表）…")
        if dry_run:
            print("【预览模式，不写入数据库】\n")

        wc = _migrate_words(db, dry_run)
        qc = _migrate_questions(db, dry_run)
        wrong_c = _migrate_wrong(db, dry_run)
        detail_c = _migrate_answer_details(db, dry_run)

        if not dry_run:
            db.commit()
            print("\n已提交事务。")
        else:
            db.rollback()

        print(
            f"\n处理完成：字库 {wc} 条，题目 {qc} 条，错题 {wrong_c} 条，作答明细 {detail_c} 条。"
        )
    except Exception as e:
        db.rollback()
        print(f"迁移失败: {e}")
        raise
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="拼音迁移为声调符号并填充多音字")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅打印变更预览，不写入数据库",
    )
    args = parser.parse_args()
    run_migration(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
