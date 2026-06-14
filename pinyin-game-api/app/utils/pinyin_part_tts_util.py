"""声母/韵母格子 TTS 朗读文本（汉语拼音认读，避免拉丁字母被读成英文）。

认读字来源：http://www.hanyupinyin.cn/ 首页声母表、韵母表（可用
`python -m app.scripts.scrape_hanyupinyin_cn` 重新抓取并生成 JSON）。
edge-tts 对单独字母会按英文读，故合成时使用下列汉字。
"""

from __future__ import annotations

from typing import Optional

# 与 hanyupinyin.cn 声母表一致（玻坡摸佛 …）
INITIAL_TTS_CHARS: dict[str, str] = {
    "b": "玻",
    "p": "坡",
    "m": "摸",
    "f": "佛",
    "d": "得",
    "t": "特",
    "n": "讷",
    "l": "勒",
    "g": "歌",
    "k": "科",
    "h": "喝",
    "j": "基",
    "q": "欺",
    "x": "希",
    "zh": "知",
    "ch": "蚩",
    "sh": "思",
    "r": "日",
    "z": "资",
    "c": "雌",
    "s": "思",
    "y": "衣",
    "w": "乌",
}

# 与 hanyupinyin.cn 韵母表一致；游戏中 ü 记为 v
FINAL_TTS_CHARS: dict[str, str] = {
    "a": "啊",
    "o": "喔",
    "e": "鹅",
    "i": "衣",
    "u": "乌",
    "v": "迂",
    "ai": "哀",
    "ei": "诶",
    "ui": "威",
    "ao": "熬",
    "ou": "欧",
    "iu": "优",
    "ie": "耶",
    "ve": "约",
    "er": "耳",
    "an": "安",
    "en": "恩",
    "in": "因",
    "un": "温",
    "vn": "晕",
    "ang": "昂",
    "eng": "享",
    "ing": "英",
    "ong": "翁",
    # 以下为本项目额外韵母，站点无 mp3，仅用 TTS 认读字近似
    "ia": "呀",
    "iao": "腰",
    "ian": "烟",
    "iang": "羊",
    "iong": "用",
    "ua": "蛙",
    "uo": "窝",
    "uai": "歪",
    "uan": "弯",
    "uang": "王",
    "ue": "约",
}

# 站点提供标准 mp3 的部件（与 /mp3/{key}.mp3 一致）
HANYUPINYIN_CN_MP3_INITIALS = frozenset(INITIAL_TTS_CHARS.keys())
HANYUPINYIN_CN_MP3_FINALS = frozenset(
    {
        "a",
        "o",
        "e",
        "i",
        "u",
        "v",
        "ai",
        "ei",
        "ui",
        "ao",
        "ou",
        "iu",
        "ie",
        "ve",
        "er",
        "an",
        "en",
        "in",
        "un",
        "vn",
        "ang",
        "eng",
        "ing",
        "ong",
    }
)


def part_mp3_filename(part: str, *, is_initial: bool) -> Optional[str]:
    """hanyupinyin.cn 上的 mp3 文件名，无则 None。"""
    key = (part or "").strip()
    if is_initial:
        if not key:
            return None
        return f"{key}.mp3" if key in HANYUPINYIN_CN_MP3_INITIALS else None
    norm = key.lower().replace("ü", "v").replace("ɑ", "a")
    if not norm:
        return None
    return f"{norm}.mp3" if norm in HANYUPINYIN_CN_MP3_FINALS else None


def part_to_tts_speak_text(part: str, *, is_initial: bool) -> Optional[str]:
    """
    将格子上的声母/韵母转为 TTS 合成用汉字。

    Args:
        part: 格子值，如 b、iang；无声母为空串。
        is_initial: True 表示声母，False 表示韵母。

    Returns:
        用于 edge-tts 的文本；无法映射时返回 None。
    """
    key = (part or "").strip()
    if is_initial:
        if not key:
            return "无"
        return INITIAL_TTS_CHARS.get(key)

    if not key:
        return None
    norm = key.lower().replace("ü", "v").replace("ɑ", "a")
    return FINAL_TTS_CHARS.get(norm)
