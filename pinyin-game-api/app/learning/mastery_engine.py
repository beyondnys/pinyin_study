"""掌握度纯逻辑：权重计算与答对/答错状态迁移。"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from app.learning import config as cfg
from app.learning.types import MasteryRowData, MasteryState


def default_row() -> MasteryRowData:
    """未学习过的默认状态。"""
    return MasteryRowData(state=MasteryState.UNSEEN)


def interval_days_for_streak(correct_streak: int) -> int:
    """根据连续答对次数返回下次复习间隔（天）。"""
    if correct_streak <= 0:
        return 0
    idx = min(correct_streak - 1, len(cfg.REVIEW_INTERVALS_DAYS) - 1)
    return cfg.REVIEW_INTERVALS_DAYS[idx]


def compute_sample_weight(row: Optional[MasteryRowData], now: datetime) -> tuple[float, MasteryState]:
    """
    计算单题抽样权重与展示用状态。
    权重越高越容易被抽到；已掌握且未到复习时间的题权重接近 W_FLOOR。
    """
    if row is None or row.state == MasteryState.UNSEEN:
        return cfg.W_UNSEEN, MasteryState.UNSEEN

    if row.state == MasteryState.LEARNING:
        w = cfg.W_LEARNING * (1.0 + min(row.wrong_count, cfg.WRONG_COUNT_BOOST_CAP) * cfg.WRONG_COUNT_BOOST)
        if row.last_wrong_at:
            hours = (now - row.last_wrong_at).total_seconds() / 3600.0
            if hours < cfg.RECENT_WRONG_HOURS:
                w *= cfg.RECENT_WRONG_MULTIPLIER
        return max(cfg.W_FLOOR, w), MasteryState.LEARNING

    # mastered
    if row.next_review_at is None or now >= row.next_review_at:
        return max(cfg.W_FLOOR, cfg.W_DUE_REVIEW), MasteryState.MASTERED

    # 未到复习日：在 [W_FLOOR, W_MASTERED] 之间随剩余时间升高
    remaining = (row.next_review_at - now).total_seconds()
    max_span = max(cfg.REVIEW_INTERVALS_DAYS[-1], 1) * 86400.0
    ratio = min(1.0, max(0.0, remaining / max_span))
    w = cfg.W_FLOOR + (cfg.W_MASTERED - cfg.W_FLOOR) * ratio
    return max(cfg.W_FLOOR, w), MasteryState.MASTERED


def apply_wrong(row: MasteryRowData, now: datetime) -> MasteryRowData:
    """每次答错：累计错误、清零 streak、立即进入复习队列。"""
    row.wrong_count += 1
    row.correct_streak = 0
    row.state = MasteryState.LEARNING
    row.last_result = 0
    row.last_wrong_at = now
    row.last_practiced_at = now
    row.next_review_at = now
    return row


def apply_correct(row: MasteryRowData, now: datetime) -> MasteryRowData:
    """答对：streak+1，达阈值进入 mastered，并按间隔设置 next_review_at。"""
    row.correct_streak += 1
    row.last_result = 1
    row.last_correct_at = now
    row.last_practiced_at = now

    if row.correct_streak >= cfg.MASTERED_STREAK_THRESHOLD:
        row.state = MasteryState.MASTERED
    else:
        row.state = MasteryState.LEARNING

    days = interval_days_for_streak(row.correct_streak)
    row.next_review_at = now + timedelta(days=days)
    return row


def row_from_orm(orm_row) -> MasteryRowData:
    """ORM -> 内存结构。"""
    return MasteryRowData(
        wrong_count=orm_row.wrong_count,
        correct_streak=orm_row.correct_streak,
        state=MasteryState(orm_row.state),
        last_result=orm_row.last_result,
        last_wrong_at=orm_row.last_wrong_at,
        last_correct_at=orm_row.last_correct_at,
        last_practiced_at=orm_row.last_practiced_at,
        next_review_at=orm_row.next_review_at,
    )
