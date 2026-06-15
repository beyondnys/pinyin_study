"""TTS 业务类型常量。"""

from __future__ import annotations

# 练习册题目
BIZ_PRACTICE_QUESTION_HANZI = "practice_question_hanzi"
BIZ_PRACTICE_QUESTION_PINYIN = "practice_question_pinyin"

# 字库
BIZ_PINYIN_WORD_HANZI = "pinyin_word_hanzi"
BIZ_PINYIN_WORD_PINYIN = "pinyin_word_pinyin"

# 拼音练习游戏：声母/韵母格子朗读
BIZ_PINYIN_SELECT_PART = "pinyin_select_part"

# 词语连连看：整词朗读
BIZ_WORD_MATCH_WORD = "word_match_word"

GENERATE_PENDING = 0
GENERATE_RUNNING = 1
GENERATE_SUCCESS = 2
GENERATE_FAILED = 3
