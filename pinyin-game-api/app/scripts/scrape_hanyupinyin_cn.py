"""
从 http://www.hanyupinyin.cn/ 解析声母/韵母认读字与 mp3 文件名。

用法（在 pinyin-game-api 目录）：
    python -m app.scripts.scrape_hanyupinyin_cn
    python -m app.scripts.scrape_hanyupinyin_cn --download --out-dir ../pinyin-game-web/public/sounds/pinyin-parts
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.request
from html import unescape
from pathlib import Path
from typing import Any

HOME_URL = "http://www.hanyupinyin.cn/"
# 页面 JS 中音频目录（常见为 /yinyun/ 或 /yunyin/，以实际 HTML 为准）
DEFAULT_MP3_BASE = "http://www.hanyupinyin.cn/mp3/"


def fetch_html(url: str = HOME_URL, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "pinyin-study/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def detect_mp3_base(html: str) -> str:
    """从页面 script 推断 mp3 根路径（站点实际为 /mp3/）。"""
    patterns = [
        r"burl\s*=\s*['\"]([^'\"]+)['\"]",
        r"['\"]([^'\"]*?/mp3/)['\"]",
        r"['\"]([^'\"]*yinyun[^'\"]*)['\"]\s*\+",
        r"mp3Base\s*=\s*['\"]([^'\"]+)['\"]",
    ]
    for pat in patterns:
        m = re.search(pat, html, re.I)
        if m:
            base = m.group(1)
            if not base.startswith("http"):
                base = HOME_URL.rstrip("/") + "/" + base.lstrip("/")
            if not base.endswith("/"):
                base += "/"
            return base
    return DEFAULT_MP3_BASE


def _parse_button_group(html: str, class_name: str) -> list[dict[str, str]]:
    """解析带 mp3 属性的 <a class="button dushengmu|duyunmu"> 标签。"""
    items: list[dict[str, str]] = []
    pattern = (
        r'<a\s+[^>]*\b'
        + re.escape(class_name)
        + r'\b[^>]*\bmp3\s*=\s*["\']([^"\']+)["\'][^>]*>\s*([^<]+)'
    )
    for m in re.finditer(pattern, html, flags=re.I):
        mp3 = m.group(1)
        label = unescape(m.group(2).strip())
        # 去掉喇叭图标等残留空白
        label = re.sub(r"\s+", " ", label).strip()
        parts = label.split(None, 1)
        pinyin_key = parts[0].strip() if parts else ""
        hanzi = parts[1].strip() if len(parts) > 1 else ""
        items.append(
            {
                "key": pinyin_key,
                "hanzi": hanzi,
                "mp3": mp3.strip(),
                "label": label,
            }
        )
    return items


def parse_page(html: str) -> dict[str, Any]:
    """解析首页声母表、韵母表。"""
    mp3_base = detect_mp3_base(html)
    initials = _parse_button_group(html, "dushengmu")
    finals = _parse_button_group(html, "duyunmu")
    if not finals:
        finals = _parse_button_group(html, "yuyinmu")

    return {
        "source": HOME_URL,
        "mp3_base": mp3_base,
        "initials": initials,
        "finals": finals,
    }


def build_tts_maps(data: dict[str, Any]) -> dict[str, dict[str, str]]:
    """生成与 pinyin_part_tts_util 一致的 initial/final 汉字映射。"""
    initial_map: dict[str, str] = {}
    for row in data.get("initials", []):
        key = row["key"].strip()
        hanzi = row.get("hanzi", "").strip()
        if key and hanzi:
            initial_map[key] = hanzi

    final_map: dict[str, str] = {}
    for row in data.get("finals", []):
        key = row["key"].strip().lower().replace("ü", "v").replace("ɑ", "a")
        hanzi = row.get("hanzi", "").strip()
        if key and hanzi:
            final_map[key] = hanzi

    return {"initials": initial_map, "finals": final_map}


def download_mp3(mp3_base: str, filename: str, out_dir: Path) -> bool:
    url = mp3_base.rstrip("/") + "/" + filename.lstrip("/")
    out_path = out_dir / filename
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists() and out_path.stat().st_size > 0:
        return True
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "pinyin-study/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            out_path.write_bytes(resp.read())
        return True
    except urllib.error.HTTPError as e:
        print(f"  [跳过] {url} -> HTTP {e.code}")
        return False
    except Exception as e:
        print(f"  [失败] {url} -> {e}")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="解析 hanyupinyin.cn 声母韵母表")
    parser.add_argument("--download", action="store_true", help="下载 mp3 到本地")
    parser.add_argument(
        "--out-dir",
        default="data/hanyupinyin_cn",
        help="JSON 与 mp3 输出目录（相对 pinyin-game-api）",
    )
    parser.add_argument(
        "--web-dir",
        default="../pinyin-game-web/public/sounds/pinyin-parts",
        help="同时复制 mp3 到前台静态目录（与 playLocalPartAudio 路径一致）",
    )
    args = parser.parse_args()

    html = fetch_html()
    data = parse_page(html)
    maps = build_tts_maps(data)

    out_root = Path(args.out_dir)
    out_root.mkdir(parents=True, exist_ok=True)
    json_path = out_root / "pinyin_parts.json"
    payload = {**data, "tts_maps": maps}
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已写入 {json_path}")
    print(f"声母 {len(data['initials'])} 条，韵母 {len(data['finals'])} 条")
    print(f"mp3 根路径: {data['mp3_base']}")

    if args.download:
        ok = 0
        all_mp3 = {r["mp3"] for r in data["initials"] + data["finals"] if r.get("mp3")}
        web_dir = Path(args.web_dir)
        web_dir.mkdir(parents=True, exist_ok=True)
        for name in sorted(all_mp3):
            if download_mp3(data["mp3_base"], name, out_root / "mp3"):
                ok += 1
                src = out_root / "mp3" / name
                if src.exists():
                    web_dir.mkdir(parents=True, exist_ok=True)
                    (web_dir / name).write_bytes(src.read_bytes())
        print(f"下载 mp3: {ok}/{len(all_mp3)}")
        if web_dir.exists():
            print(f"已同步到前台: {web_dir.resolve()}")

    print("\n--- 声母 TTS 映射 ---")
    for k, v in sorted(maps["initials"].items()):
        print(f"  {k!r} -> {v}")
    print("\n--- 韵母 TTS 映射 ---")
    for k, v in sorted(maps["finals"].items()):
        print(f"  {k!r} -> {v}")


if __name__ == "__main__":
    main()
