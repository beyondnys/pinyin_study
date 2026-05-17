"""自适应学习模块：类型定义。"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class ContentType(str, Enum):
    """学习内容类型，后续可扩展词语、成语等。"""

    PINYIN_PAIR = "pinyin_pair"
    WORD_CHOICE = "word_choice"
    IDIOM_CHOICE = "idiom_choice"


class MasteryState(str, Enum):
    """掌握状态。"""

    UNSEEN = "unseen"
    LEARNING = "learning"
    MASTERED = "mastered"


class ScopeType(str, Enum):
    """练习场景类型。"""

    BOOK = "book"
    GLOBAL = "global"


@dataclass(frozen=True)
class LearningScope:
    """用户 + 场景：如某本练习册。"""

    scope_type: ScopeType
    scope_id: int

    def cache_key(self) -> str:
        return f"{self.scope_type.value}:{self.scope_id}"


@dataclass(frozen=True)
class ContentRef:
    """内容项引用（不含用户）。"""

    content_type: ContentType
    content_id: int

    def item_key(self) -> str:
        return f"{self.content_type.value}:{self.content_id}"


@dataclass
class CandidateItem:
    """抽题候选项：业务载荷 + 用于掌握度的引用。"""

    content: ContentRef
    question_id: int
    hanzi: str
    pinyin: str


@dataclass
class MasteryRowData:
    """掌握度行（内存结构，与 ORM 对应）。"""

    wrong_count: int = 0
    correct_streak: int = 0
    state: MasteryState = MasteryState.UNSEEN
    last_result: Optional[int] = None
    last_wrong_at: Optional[datetime] = None
    last_correct_at: Optional[datetime] = None
    last_practiced_at: Optional[datetime] = None
    next_review_at: Optional[datetime] = None


@dataclass
class WeightedCandidate:
    """带权重的候选项。"""

    item: CandidateItem
    weight: float
    state: MasteryState
