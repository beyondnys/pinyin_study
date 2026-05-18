"""
为已入库的字库、题目批量生成 TTS（汉字 + 拼音）。

用法（在 pinyin-game-api 目录下，需配置 .env 中 MinIO 与 TTS）：
    python -m app.scripts.backfill_tts_audio
    python -m app.scripts.backfill_tts_audio --scope questions --limit 100
    python -m app.scripts.backfill_tts_audio --scope words --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.database import SessionLocal
from app.models.practice_question import PracticeQuestion
from app.models.word_library import WordLibrary
from app.services.tts.tts_audio_service import generate_tts_for_question, generate_tts_for_word


async def backfill_questions(db, limit: int, dry_run: bool) -> int:
    rows = (
        db.query(PracticeQuestion)
        .filter(PracticeQuestion.is_deleted == 0)
        .order_by(PracticeQuestion.id.asc())
        .limit(limit)
        .all()
    )
    n = 0
    for q in rows:
        if dry_run:
            print(f"  [题目] id={q.id} {q.hanzi} / {q.pinyin}")
        else:
            await generate_tts_for_question(db, q.id, q.hanzi, q.pinyin)
        n += 1
    return n


async def backfill_words(db, limit: int, dry_run: bool) -> int:
    rows = (
        db.query(WordLibrary)
        .filter(WordLibrary.is_deleted == 0)
        .order_by(WordLibrary.id.asc())
        .limit(limit)
        .all()
    )
    n = 0
    for w in rows:
        if dry_run:
            print(f"  [字库] id={w.id} {w.hanzi} / {w.pinyin}")
        else:
            await generate_tts_for_word(db, w.id, w.hanzi, w.pinyin)
        n += 1
    return n


async def run_async(scope: str, limit: int, dry_run: bool) -> None:
    db = SessionLocal()
    try:
        qc = wc = 0
        if scope in ("all", "questions"):
            print(f"处理题目（最多 {limit} 条）…")
            qc = await backfill_questions(db, limit, dry_run)
        if scope in ("all", "words"):
            print(f"处理字库（最多 {limit} 条）…")
            wc = await backfill_words(db, limit, dry_run)
        print(f"\n完成：题目 {qc} 条，字库 {wc} 条" + ("（预览，未写入）" if dry_run else ""))
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="回填已入库汉字/拼音的 TTS 音频")
    parser.add_argument(
        "--scope",
        choices=["all", "questions", "words"],
        default="all",
        help="处理范围",
    )
    parser.add_argument("--limit", type=int, default=500, help="每类最多处理条数")
    parser.add_argument("--dry-run", action="store_true", help="仅预览")
    args = parser.parse_args()
    asyncio.run(run_async(args.scope, args.limit, args.dry_run))


if __name__ == "__main__":
    main()
