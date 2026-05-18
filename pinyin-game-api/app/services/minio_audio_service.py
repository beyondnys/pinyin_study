"""MinIO 音频上传与预签名访问。"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from functools import lru_cache
from urllib.parse import urlparse

from minio import Minio
from minio.error import S3Error

from app.config import settings
from app.utils.text_hash_util import build_text_hash

logger = logging.getLogger(__name__)

_ACCESS_DENIED_HINT = (
    "MinIO AccessDenied：请在控制台 https://console-minio.beyondttyy.top 创建桶 "
    f"「{settings.MINIO_BUCKET}」，并为用户 {settings.MINIO_ACCESS_KEY} 配置该桶的读写策略"
    "（s3:PutObject、s3:GetObject；若开启自动建桶还需 s3:CreateBucket）。"
    "也可在 .env 将 MINIO_BUCKET 改为你已有权限的桶名。"
)


def _validate_minio_config() -> None:
    """上传前校验 MinIO 配置。"""
    if not (settings.MINIO_ACCESS_KEY or "").strip():
        raise ValueError(
            "MINIO_ACCESS_KEY 未配置，请在 pinyin-game-api/.env 中设置（可参考 .env.example）"
        )
    if not (settings.MINIO_SECRET_KEY or "").strip():
        raise ValueError(
            "MINIO_SECRET_KEY 未配置，请在 pinyin-game-api/.env 中设置 MinIO 密码"
        )


def _client() -> Minio:
    _validate_minio_config()
    endpoint = settings.MINIO_ENDPOINT.strip()
    secure = settings.MINIO_SECURE
    if endpoint.startswith("http://"):
        parsed = urlparse(endpoint)
        endpoint = parsed.netloc or parsed.path
        secure = False
    elif endpoint.startswith("https://"):
        parsed = urlparse(endpoint)
        endpoint = parsed.netloc or parsed.path
        secure = True
    return Minio(
        endpoint,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=secure,
        region=settings.MINIO_REGION,
    )


def _raise_s3_error(exc: S3Error, action: str) -> None:
    """将 S3 错误转为可读提示并抛出。"""
    code = getattr(exc, "code", "") or ""
    if code in ("AccessDenied", "AccessDeniedException"):
        raise ValueError(f"{action} 失败：{_ACCESS_DENIED_HINT}") from exc
    if code in ("NoSuchBucket", "NoSuchBucketException"):
        raise ValueError(
            f"{action} 失败：桶「{settings.MINIO_BUCKET}」不存在，请在 MinIO 控制台创建该桶"
        ) from exc
    raise ValueError(f"{action} 失败: {exc}") from exc


@lru_cache(maxsize=1)
def _ensure_bucket_once() -> None:
    """
    可选：检查并创建桶（需 ListBucket/HeadBucket/CreateBucket 权限）。
    默认关闭，直接 PutObject，避免 bucket_exists 触发 AccessDenied。
    """
    if not settings.MINIO_AUTO_CREATE_BUCKET:
        return
    client = _client()
    bucket = settings.MINIO_BUCKET
    try:
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)
    except S3Error as e:
        _raise_s3_error(e, "检查/创建存储桶")


def build_object_name(voice_name: str, text: str) -> str:
    """tts/{voice_name}/{yyyy}/{MM}/{dd}/{text_hash}.mp3"""
    now = datetime.utcnow()
    text_hash = build_text_hash(text, voice_name)
    safe_voice = voice_name.replace("/", "_")
    return f"tts/{safe_voice}/{now:%Y/%m/%d}/{text_hash}.mp3"


def upload_audio_file(
    local_file_path: str,
    object_name: str,
    content_type: str = "audio/mpeg",
) -> str:
    """
    上传音频到 MinIO。
    :return: object_name
    """
    _ensure_bucket_once()
    client = _client()
    bucket = settings.MINIO_BUCKET
    try:
        client.fput_object(
            bucket,
            object_name,
            local_file_path,
            content_type=content_type,
        )
    except S3Error as e:
        _raise_s3_error(e, "上传音频")
    return object_name


def get_presigned_audio_url(object_name: str, bucket: str | None = None) -> str:
    """生成预签名 GET URL（公网访问）。"""
    client = _client()
    bkt = bucket or settings.MINIO_BUCKET
    try:
        return client.presigned_get_object(
            bkt,
            object_name,
            expires=timedelta(seconds=settings.MINIO_PRESIGN_EXPIRE_SECONDS),
        )
    except S3Error as e:
        _raise_s3_error(e, "生成预签名链接")
