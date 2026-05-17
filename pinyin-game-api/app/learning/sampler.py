"""加权无放回抽样。"""

from __future__ import annotations

import random
from typing import List, TypeVar

from app.learning import config as cfg
from app.learning.types import MasteryState, WeightedCandidate

T = TypeVar("T")


def weighted_sample_without_replacement(
    candidates: List[WeightedCandidate],
    pick_count: int,
    *,
    min_learning: int = cfg.MIN_LEARNING_IN_SESSION,
) -> List[WeightedCandidate]:
    """
    按权重无放回抽取 pick_count 项。
    若存在 learning 状态题目，尽量保证至少 min_learning 道（不足则全抽 learning）。
    """
    if not candidates:
        return []
    k = min(pick_count, len(candidates))
    if k <= 0:
        return []

    pool = list(candidates)
    selected: List[WeightedCandidate] = []

    learning_in_pool = [c for c in pool if c.state == MasteryState.LEARNING]
    if learning_in_pool and min_learning > 0 and k >= min_learning:
        need = min(min_learning, len(learning_in_pool), k)
        for _ in range(need):
            weights = [c.weight for c in learning_in_pool]
            chosen = random.choices(learning_in_pool, weights=weights, k=1)[0]
            selected.append(chosen)
            learning_in_pool.remove(chosen)
            pool.remove(chosen)
        k -= need

    while pool and len(selected) < pick_count:
        weights = [max(c.weight, cfg.W_FLOOR) for c in pool]
        total = sum(weights)
        if total <= 0:
            idx = random.randrange(len(pool))
        else:
            idx = random.choices(range(len(pool)), weights=weights, k=1)[0]
        selected.append(pool.pop(idx))

    return selected
