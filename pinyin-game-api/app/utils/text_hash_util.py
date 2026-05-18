"""文本标准化与 Hash 工具（TTS 去重）。"""

from __future__ import annotations

import hashlib
import re


def normalize_text(text: str) -> str:
    """
    去掉前后空格，合并连续空白字符。
    空文本返回空字符串。
    """
    if not text:
        return ""
    return re.sub(r"\s+", " ", text.strip())


def build_text_hash(text: str, voice_name: str) -> str:
    """SHA256(normalized_text + ':' + voice_name)。"""
    normalized = normalize_text(text)
    raw = f"{normalized}:{voice_name.strip()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
