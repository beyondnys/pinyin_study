"""应用配置，从环境变量读取。"""

from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """全局配置项。"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DATABASE_URL: str = "mysql+pymysql://root:password@127.0.0.1:3306/pinyin_game?charset=utf8mb4"
    REDIS_URL: str = "redis://127.0.0.1:6379/0"
    JWT_SECRET: str = "dev-secret-change-in-production"
    JWT_EXPIRE_DAYS: int = 7
    SINGLE_LOGIN: bool = False
    CORS_ORIGINS: str = "*"


settings = Settings()
