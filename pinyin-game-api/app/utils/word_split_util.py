"""词语连连看：词语校验与按字拆分。"""

from __future__ import annotations

MIN_WORD_LEN = 2
MAX_WORD_LEN = 4
MAX_TOTAL_CARDS = 16
# 4 列 × 4 行时最多空 1 格
MIN_GRID_FILL_CARDS = 15
GRID_COLS = 4
DEFAULT_PICK_WORDS = 8
MIN_PICK_WORDS = 3
MAX_PICK_WORDS = 8


def normalize_word(text: str) -> str:
    """去掉首尾空白。"""
    return (text or "").strip()


def validate_word(text: str) -> str:
    """
    校验词语：2～4 个汉字，不含空格与标点。
    :raises ValueError: 不合法时
    """
    word = normalize_word(text)
    if not word:
        raise ValueError("词语不能为空")
    if len(word) < MIN_WORD_LEN or len(word) > MAX_WORD_LEN:
        raise ValueError(f"词语长度须为 {MIN_WORD_LEN}～{MAX_WORD_LEN} 字")
    for ch in word:
        if not ("\u4e00" <= ch <= "\u9fff"):
            raise ValueError(f"词语须为汉字：{word}")
    return word


def split_word_chars(word: str) -> list[str]:
    """将词语拆为单字列表，顺序与原文一致。"""
    validated = validate_word(word)
    return list(validated)


def total_cards_for_words(words: list[str]) -> int:
    """计算一组词的总卡数（每字一卡）。"""
    return sum(len(w) for w in words)


def trim_words_to_card_limit(words: list[tuple[int, str, int]], max_cards: int = MAX_TOTAL_CARDS) -> list[tuple[int, str, int]]:
    """
    在不超过 max_cards 的前提下保留尽可能多的词。
    words: [(question_id, word, word_len), ...]
    """
    picked: list[tuple[int, str, int]] = []
    total = 0
    for item in words:
        qid, word, wlen = item
        if total + wlen > max_cards:
            break
        picked.append(item)
        total += wlen
    return picked


def _better_word_subset(
    a: tuple[int, ...],
    b: tuple[int, ...],
) -> bool:
    """同总卡数时优先词数更多；词数相同则优先权重更靠前（下标更小）。"""
    if len(a) != len(b):
        return len(a) > len(b)
    return a < b


def pick_words_for_full_grid(
    items: list[tuple[int, str, int]],
    *,
    max_cards: int = MAX_TOTAL_CARDS,
    min_fill: int = MIN_GRID_FILL_CARDS,
    min_words: int = MIN_PICK_WORDS,
    max_words: int = MAX_PICK_WORDS,
    pool_limit: int = 24,
) -> list[tuple[int, str, int]]:
    """
    从候选中选取一组词，使总卡数尽量为 16（其次 15），4×4 棋盘最多空 1 格。
    items 须按掌握度权重从高到低排列。
    同卡数时优先词数更多（利于 2 字词填满）。
    """
    if not items:
        return []

    pool = items[: min(len(items), pool_limit)]

    # dp[total] = 选中的 pool 下标元组
    dp: dict[int, tuple[int, ...]] = {0: ()}

    for i, (_, _, wlen) in enumerate(pool):
        next_dp = dict(dp)
        for total, idxs in dp.items():
            nt = total + wlen
            if nt > max_cards:
                continue
            new_idxs = idxs + (i,)
            if len(new_idxs) > max_words:
                continue
            prev = next_dp.get(nt)
            if prev is None or _better_word_subset(new_idxs, prev):
                next_dp[nt] = new_idxs
        dp = next_dp

    valid = [(t, idxs) for t, idxs in dp.items() if idxs and len(idxs) >= min_words]
    if not valid:
        return trim_words_to_card_limit(items, max_cards)

    # 优先 16、15，其次取最大总卡数
    for target in range(max_cards, min_fill - 1, -1):
        match = next(((t, idxs) for t, idxs in valid if t == target), None)
        if match:
            _, idxs = match
            return [pool[i] for i in idxs]

    best_total = max(t for t, _ in valid)
    idxs = dp[best_total]
    return [pool[i] for i in idxs]
