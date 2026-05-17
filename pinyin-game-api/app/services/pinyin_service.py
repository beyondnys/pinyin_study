"""拼音生成服务，基于 pypinyin。"""

from __future__ import annotations
import re

from pypinyin import Style, pinyin


def is_hanzi(char: str) -> bool:
    """判断单个字符是否为汉字。"""
    return bool(re.match(r"[\u4e00-\u9fff]", char))


def extract_unique_hanzi(text: str) -> list[str]:
    """从文本中提取不重复汉字，保持出现顺序。"""
    seen = set()
    result = []
    for c in text:
        if is_hanzi(c) and c not in seen:
            seen.add(c)
            result.append(c)
    return result


def hanzi_to_pinyin(hanzi: str) -> tuple[str, str]:
    """
    将汉字转为拼音。
    返回 (带声调拼音, 无声调拼音)。
    """
    if not hanzi:
        return "", ""
    tone3 = pinyin(hanzi, style=Style.TONE3, heteronym=False)
    normal = pinyin(hanzi, style=Style.NORMAL, heteronym=False)
    py_tone = "".join(x[0] for x in tone3) if tone3 else ""
    py_plain = "".join(x[0] for x in normal) if normal else ""
    return py_tone, py_plain
