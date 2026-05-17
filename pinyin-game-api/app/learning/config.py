"""自适应学习：权重与间隔参数（可调）。"""

from __future__ import annotations

# ---------- 抽样权重 ----------
# 从未出现
W_UNSEEN = 1.0
# 学习中 / 错题（基础）
W_LEARNING = 3.0
# 每次历史错误叠加系数（ capped ）
WRONG_COUNT_BOOST = 0.15
WRONG_COUNT_BOOST_CAP = 10
# 24 小时内再次答错加权
RECENT_WRONG_HOURS = 24
RECENT_WRONG_MULTIPLIER = 1.35
# 已掌握但未到复习时间
W_MASTERED = 0.35
# 已到复习时间（间隔到期）
W_DUE_REVIEW = 1.15
# 全局最小权重（保证仍会被抽到）
W_FLOOR = 0.08

# 连续答对 N 次进入 mastered
MASTERED_STREAK_THRESHOLD = 2

# 答对后的复习间隔（天），按 correct_streak 索引，超出取最后一档
REVIEW_INTERVALS_DAYS = [0, 1, 3, 7, 14, 30, 60]

# 每局至少包含 1 道「学习中」题（若候选池里有）
MIN_LEARNING_IN_SESSION = 1
