"""拼音练习游戏 Schema。"""

from typing import Optional

from pydantic import BaseModel, Field


class NextQuestionOut(BaseModel):
    """出题：不含正确答案。"""

    question_id: int
    hanzi: str
    audio_url: Optional[str] = None
    index_no: int = 1
    # 本题标准答案无声母时为 True，前台可直接选韵母（不展示「无」）
    zero_initial: bool = False


class AnswerIn(BaseModel):
    """提交用户选择的声母、韵母、声调。"""

    question_id: int
    initial: str = ""
    final: str
    tone: int = Field(ge=1, le=5)
    duration_ms: int = Field(ge=0, default=0)
    session_id: Optional[str] = None


class AnswerOut(BaseModel):
    """判题结果。"""

    is_correct: bool
    score_delta: int
    total_score: int
    correct_initial: str
    correct_final: str
    correct_tone: int
    pinyin_display: str
    hanzi: str


class PartAudioOut(BaseModel):
    """声母/韵母朗读。"""

    text: str
    audio_url: Optional[str] = None


class StatisticsOut(BaseModel):
    """答题统计。"""

    total_count: int
    correct_count: int
    accuracy: float
    total_score: int
