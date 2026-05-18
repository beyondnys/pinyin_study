"""拼音列表序列化与答案比对工具。"""

from __future__ import annotations

import json
from typing import Iterable, List


def encode_pinyin_list(items: Iterable[str]) -> str:
    """将读音列表序列化为 JSON 字符串存入数据库。"""
    cleaned = []
    seen: set[str] = set()
    for x in items:
        s = (x or "").strip()
        if not s or s in seen:
            continue
        seen.add(s)
        cleaned.append(s)
    return json.dumps(cleaned, ensure_ascii=False)


def decode_pinyin_list(raw: str | None) -> List[str]:
    """从数据库 JSON 字段解析读音列表；失败时返回空列表。"""
    if not raw or not raw.strip():
        return []
    try:
        data = json.loads(raw)
        if not isinstance(data, list):
            return []
        return [str(x).strip() for x in data if str(x).strip()]
    except (json.JSONDecodeError, TypeError):
        return []


def normalize_pinyin_for_compare(text: str) -> str:
    """比对前规范化：去空白、转小写（声调字母保留）。"""
    return (text or "").strip().lower()


def word_to_out_dict(word) -> dict:
    """字库 ORM -> API 字典（含解析后的 pinyin_list）。"""
    from app.schemas.word import WordOut

    return WordOut(
        id=word.id,
        hanzi=word.hanzi,
        pinyin=word.pinyin,
        pinyin_list=pinyin_list_for_api(word.pinyin, word.pinyin_list),
        pinyin_plain=word.pinyin_plain,
        remark=word.remark,
    ).model_dump()


def question_to_out_dict(question) -> dict:
    """题目 ORM -> API 字典。"""
    from app.schemas.question import QuestionOut

    return QuestionOut(
        id=question.id,
        book_id=question.book_id,
        hanzi=question.hanzi,
        pinyin=question.pinyin,
        pinyin_list=pinyin_list_for_api(question.pinyin, question.pinyin_list),
        sort_order=question.sort_order,
    ).model_dump()


def apply_pinyin_fields(entity, result, manual_pinyin: str | None = None) -> None:
    """
    将 PinyinResult 写入字库/题目实体（需有 pinyin、pinyin_list、pinyin_plain 字段）。
    manual_pinyin 非空时作为主读音并并入多音字列表。
    """
    if manual_pinyin and manual_pinyin.strip():
        primary = manual_pinyin.strip()
        lst = list(result.pinyin_list)
        if primary not in lst:
            lst.insert(0, primary)
        entity.pinyin = primary
        entity.pinyin_list = encode_pinyin_list(lst if lst else [primary])
    else:
        entity.pinyin = result.pinyin
        entity.pinyin_list = result.pinyin_list_json
    entity.pinyin_plain = result.pinyin_plain


def pinyin_list_for_api(primary: str, pinyin_list_json: str | None = None) -> List[str]:
    """API 返回用：解析 JSON 列表，空则回退为主读音。"""
    pl = decode_pinyin_list(pinyin_list_json)
    if pl:
        return pl
    return [primary] if primary else []


def is_pinyin_match(user_pinyin: str, primary: str, pinyin_list_json: str | None = None) -> bool:
    """
    判断用户提交的拼音是否与标准答案一致。
    支持多音字：primary 或 pinyin_list 中任一读音均判对。
    """
    user = normalize_pinyin_for_compare(user_pinyin)
    if not user:
        return False
    candidates: list[str] = []
    if primary:
        candidates.append(primary)
    candidates.extend(decode_pinyin_list(pinyin_list_json))
    seen: set[str] = set()
    for c in candidates:
        key = normalize_pinyin_for_compare(c)
        if not key or key in seen:
            continue
        seen.add(key)
        if user == key:
            return True
    return False
