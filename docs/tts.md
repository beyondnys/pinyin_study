# TTS 语音（edge-tts + MinIO）

## 能力说明

- 导入汉字/题目后自动生成 **汉字** 与 **拼音** 两条 MP3，上传 MinIO，元数据写入 `tts_audio_resource`。
- 接口返回 **预签名 URL**（公网 `https://minio.beyondttyy.top`），前端点击播放，不实时合成。
- 引擎可配置：`TTS_PROVIDER=edge`（预留替换）。

## 数据库

```bash
mysql -u root -p pinyin_game < sql/migrate_tts_audio.sql
```

## 环境变量（`.env`）

```env
MINIO_ENDPOINT=minio.beyondttyy.top
MINIO_ACCESS_KEY=admin
MINIO_SECRET_KEY=你的密钥
MINIO_BUCKET=tts
MINIO_SECURE=true
MINIO_PRESIGN_EXPIRE_SECONDS=604800

TTS_DEFAULT_VOICE=zh-CN-XiaoxiaoNeural
TTS_MAX_TEXT_LEN=200
TTS_TIMEOUT_SECONDS=60
```

## 回填已入库数据

```bash
cd pinyin-game-api
pip install -r requirements.txt
python -m app.scripts.backfill_tts_audio --dry-run
python -m app.scripts.backfill_tts_audio --scope all --limit 500
```

## 管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/admin/tts/{id}` | 查询资源 |
| POST | `/api/admin/tts/{id}/retry` | 按 ID 重试 |
| POST | `/api/admin/tts/retry-by-biz` | 按 biz_type + biz_id 重试 |

## biz_type

- `practice_question_hanzi` / `practice_question_pinyin`
- `pinyin_word_hanzi` / `pinyin_word_pinyin`

## 常见错误

### `Secret key must not be empty`

说明 **未读取到 `MINIO_SECRET_KEY`**。在 `pinyin-game-api` 目录：

```bash
cp .env.example .env
# 编辑 .env，填写：
# MINIO_SECRET_KEY=你的MinIO密码
```

确认 `.env` 与运行脚本的目录一致，然后重试：

```bash
python -m app.scripts.backfill_tts_audio --scope questions --limit 1
```

成功后 `tts_audio_resource.generate_status` 应为 `2`，且 `audio_object_name` 非空。

### `AccessDenied` / 桶权限不足

密钥已配置，但当前用户对桶 **没有读写权限**，或 `.env` 中 `MINIO_BUCKET` 与控制台桶名不一致。

本项目默认使用已有桶 **`tts`**（对象路径仍为 `tts/{音色}/{年}/{月}/{日}/{hash}.mp3`）。

**请确认：**

1. MinIO 控制台 https://console-minio.beyondttyy.top 中存在桶 **`tts`**
2. `.env` 中：`MINIO_BUCKET=tts`
3. 用户 `admin` 对 `tts/*` 有 `PutObject`、`GetObject` 权限

```env
MINIO_AUTO_CREATE_BUCKET=false
```

**验证上传（mc）：**

```bash
mc alias set myminio https://minio.beyondttyy.top admin '你的密码'
mc cp test.mp3 myminio/tts/test/test.mp3
```
