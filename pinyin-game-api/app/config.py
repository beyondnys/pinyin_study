"""应用配置，从环境变量读取。"""

from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """全局配置项。"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DATABASE_URL: str = "mysql+pymysql://pinyin_game:pinyin_game_nys@127.0.0.1:3306/pinyin_game?charset=utf8mb4"
    REDIS_URL: str = "redis://:redis123@127.0.0.1:6379/0"
    JWT_SECRET: str = "dev-secret-change-in-production"
    JWT_EXPIRE_DAYS: int = 7
    SINGLE_LOGIN: bool = False
    CORS_ORIGINS: str = "*"

    # MinIO（S3 兼容）
    MINIO_ENDPOINT: str = "minio.beyondttyy.top"
    MINIO_ACCESS_KEY: str = "admin"
    MINIO_SECRET_KEY: str = ""
    MINIO_BUCKET: str = "tts"
    MINIO_SECURE: bool = True
    MINIO_REGION: str = "us-east-1"
    MINIO_PRESIGN_EXPIRE_SECONDS: int = 7 * 24 * 3600
    # 为 true 时启动会 HeadBucket/CreateBucket（需更高权限）；生产建议在控制台先建桶
    MINIO_AUTO_CREATE_BUCKET: bool = False

    # TTS
    TTS_PROVIDER: str = "edge"
    TTS_DEFAULT_VOICE: str = "zh-CN-XiaoxiaoNeural"
    TTS_MAX_TEXT_LEN: int = 200
    TTS_TIMEOUT_SECONDS: int = 60
    TTS_ALLOWED_VOICES: str = (
        "zh-CN-XiaoxiaoNeural,zh-CN-YunxiNeural,zh-CN-YunjianNeural,zh-CN-XiaoyiNeural"
    )


settings = Settings()

