"""拼音生成服务，基于 pypinyin（声调符号 + 多音字）。"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from itertools import product
from typing import List

from pypinyin import Style, pinyin

from app.utils.pinyin_util import encode_pinyin_list

# 多音字组合上限，避免长词笛卡尔积爆炸
MAX_PINYIN_VARIANTS = 16


def is_hanzi(char: str) -> bool:
    """判断单个字符是否为汉字。"""
    return bool(re.match(r"[\u4e00-\u9fff]", char))


def extract_unique_hanzi(text: str) -> list[str]:
    """从文本中提取不重复汉字，保持出现顺序。"""
    seen = set()
    result: list[str] = []
    for c in text:
        if is_hanzi(c) and c not in seen:
            seen.add(c)
            result.append(c)
    return result


@dataclass
class PinyinResult:
    """
    汉字拼音生成结果。
    pinyin / pinyin_plain 为主读音（首选）；*_list 含全部合法读音（含多音字）。
    """

    pinyin: str
    pinyin_plain: str
    pinyin_list: List[str] = field(default_factory=list)
    pinyin_plain_list: List[str] = field(default_factory=list)

    @property
    def pinyin_list_json(self) -> str:
        """序列化后的多音字列表，可直接写入数据库。"""
        return encode_pinyin_list(self.pinyin_list)


def _dedupe_keep_order(items: List[str], limit: int) -> List[str]:
    seen: set[str] = set()
    out: List[str] = []
    for x in items:
        s = (x or "").strip()
        if not s or s in seen:
            continue
        seen.add(s)
        out.append(s)
        if len(out) >= limit:
            break
    return out


def hanzi_to_pinyin(hanzi: str, max_variants: int = MAX_PINYIN_VARIANTS) -> PinyinResult:
    """
    将汉字转为拼音（Unicode 声调符号，如 zhōng）。
    多音字时 pinyin_list 包含全部读音；多字词为各字读音的合法组合（有上限）。
    """
    text = (hanzi or "").strip()
    if not text:
        return PinyinResult(pinyin="", pinyin_plain="", pinyin_list=[], pinyin_plain_list=[])

    # 仅对汉字逐字取音；非汉字字符跳过
    chars = [c for c in text if is_hanzi(c)]
    if not chars:
        return PinyinResult(pinyin="", pinyin_plain="", pinyin_list=[], pinyin_plain_list=[])

    tone_matrix = pinyin(
        "".join(chars),
        style=Style.TONE,
        heteronym=True,
        errors=lambda x: [""],  # type: ignore[arg-type]
    )
    plain_matrix = pinyin(
        "".join(chars),
        style=Style.NORMAL,
        heteronym=True,
        errors=lambda x: [""],  # type: ignore[arg-type]
    )

    tone_combos = ["".join(parts) for parts in product(*tone_matrix) if all(parts)]
    plain_combos = ["".join(parts) for parts in product(*plain_matrix) if all(parts)]

    tone_list = _dedupe_keep_order(tone_combos, max_variants)
    plain_list = _dedupe_keep_order(plain_combos, max_variants)

    primary = tone_list[0] if tone_list else ""
    primary_plain = plain_list[0] if plain_list else ""

    return PinyinResult(
        pinyin=primary,
        pinyin_plain=primary_plain,
        pinyin_list=tone_list,
        pinyin_plain_list=plain_list,
    )


def hanzi_to_char_pinyin_list(text: str) -> List[str]:
    """
    逐字返回带声调拼音，与 text 中汉字顺序一一对应。
    用于词语连连看单字卡片展示。
    """
    result: List[str] = []
    for c in (text or ""):
        if not is_hanzi(c):
            continue
        rows = pinyin(c, style=Style.TONE, heteronym=False, errors=lambda x: [""])  # type: ignore[arg-type]
        result.append(rows[0][0] if rows and rows[0] else "")
    return result
