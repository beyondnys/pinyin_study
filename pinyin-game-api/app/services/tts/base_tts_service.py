"""TTS 抽象基类，便于后期替换引擎。"""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseTTSService(ABC):
    """TTS 引擎抽象接口。"""

    @abstractmethod
    async def generate_audio(self, text: str, output_path: str, voice_name: str) -> str:
        """
        生成音频文件到 output_path。
        :return: 输出文件路径
        :raises Exception: 生成失败时抛出明确异常
        """
