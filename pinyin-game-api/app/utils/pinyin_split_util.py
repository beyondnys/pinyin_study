"""将单字拆分为声母、韵母、声调（供拼音练习游戏判题）。"""

from __future__ import annotations

import re

from pypinyin import Style, pinyin

from app.services.pinyin_service import is_hanzi


def hanzi_to_components(hanzi: str) -> tuple[str, str, int, str]:
    """
    单字拼音拆分。

    Returns:
        (initial, final, tone, pinyin_display)
        无声母时 initial 为空串；tone 1-4，轻声为 5。
    """
    text = (hanzi or "").strip()
    if len(text) != 1 or not is_hanzi(text):
        raise ValueError("仅支持单个汉字")

    tone3_list = pinyin(text, style=Style.TONE3, strict=False, heteronym=False)
    display_list = pinyin(text, style=Style.TONE, strict=False, heteronym=False)
    ini_list = pinyin(text, style=Style.INITIALS, strict=False, heteronym=False)
    fin_list = pinyin(text, style=Style.FINALS, strict=False, heteronym=False)

    tone3 = (tone3_list[0][0] or "").lower().replace("ü", "v")
    pinyin_display = display_list[0][0] or ""
    initial = (ini_list[0][0] or "").strip()
    final = (fin_list[0][0] or "").strip()

    tone_match = re.search(r"([1-5])$", tone3)
    tone = int(tone_match.group(1)) if tone_match else 1

    if not final:
        body = re.sub(r"[1-5]$", "", tone3)
        if initial and body.startswith(initial):
            final = body[len(initial) :]
        else:
            final = body

    return initial, final, tone, pinyin_display


def compose_plain_pinyin(initial: str, final: str, tone: int) -> str:
    """组合无声调数字的拼音主体（展示用）。"""
    return f"{initial or ''}{final or ''}"
