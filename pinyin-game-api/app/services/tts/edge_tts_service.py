"""edge-tts 实现。"""

from __future__ import annotations

import asyncio
import os
from typing import Optional

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

        def _build_communicate() -> edge_tts.Communicate:
            kwargs = {
                "text": text.strip(),
                "voice": voice_name,
                "connect_timeout": settings.TTS_CONNECT_TIMEOUT_SECONDS,
                "receive_timeout": settings.TTS_RECEIVE_TIMEOUT_SECONDS,
            }
            try:
                return edge_tts.Communicate(**kwargs)
            except TypeError:
                kwargs.pop("connect_timeout", None)
                kwargs.pop("receive_timeout", None)
                return edge_tts.Communicate(**kwargs)

        async def _run(communicate: edge_tts.Communicate) -> None:
            await communicate.save(output_path)

        attempts = max(1, settings.TTS_RETRY_ATTEMPTS)
        last_error: Optional[Exception] = None
        for attempt in range(1, attempts + 1):
            try:
                communicate = _build_communicate()
                await asyncio.wait_for(_run(communicate), timeout=settings.TTS_TIMEOUT_SECONDS)
                return output_path
            except asyncio.TimeoutError as e:
                last_error = TimeoutError(f"TTS 生成超时（{settings.TTS_TIMEOUT_SECONDS}s）")
            except Exception as e:
                last_error = RuntimeError(f"edge-tts 生成失败: {e}")

            try:
                if os.path.exists(output_path):
                    os.remove(output_path)
            except OSError:
                pass

            if attempt < attempts:
                await asyncio.sleep(settings.TTS_RETRY_DELAY_SECONDS)

        raise last_error or RuntimeError("edge-tts 生成失败")
