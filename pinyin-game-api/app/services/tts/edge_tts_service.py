"""edge-tts 实现。"""

from __future__ import annotations

import asyncio

import edge_tts

from app.config import settings
from app.services.tts.base_tts_service import BaseTTSService


class EdgeTTSService(BaseTTSService):
    """使用 Microsoft Edge TTS 在线合成。"""

    async def generate_audio(self, text: str, output_path: str, voice_name: str) -> str:
        if not text or not text.strip():
            raise ValueError("TTS 文本不能为空")
        allowed = {v.strip() for v in settings.TTS_ALLOWED_VOICES.split(",") if v.strip()}
        if voice_name not in allowed:
            raise ValueError(f"不支持的音色: {voice_name}")

        communicate = edge_tts.Communicate(text=text.strip(), voice=voice_name)

        async def _run() -> None:
            await communicate.save(output_path)

        try:
            await asyncio.wait_for(_run(), timeout=settings.TTS_TIMEOUT_SECONDS)
        except asyncio.TimeoutError as e:
            raise TimeoutError(f"TTS 生成超时（{settings.TTS_TIMEOUT_SECONDS}s）") from e
        except Exception as e:
            raise RuntimeError(f"edge-tts 生成失败: {e}") from e

        return output_path
