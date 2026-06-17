# TTS 语音（edge-tts + MinIO）

## 能力说明

- 导入汉字/题目后自动生成 **汉字** 与 **拼音** 两条 MP3，上传 MinIO，元数据写入 `tts_audio_resource`。
- 接口返回 **预签名 URL**（公网 `https://minio.beyondttyy.top`），前端点击播放，不实时合成。
- **拼音练习游戏**：点击声母/韵母格子优先播放本地标准 mp3（来自 [hanyupinyin.cn](http://www.hanyupinyin.cn/)），路径 `pinyin-game-web/public/sounds/pinyin-parts/{key}.mp3`；无本地文件时再调用 `GET /api/game/pinyin-select/part-audio`（edge-tts + MinIO）。认读字映射见 `app/utils/pinyin_part_tts_util.py`。
- **抓取官网读音**：在 `pinyin-game-api` 目录执行 `python -m app.scripts.scrape_hanyupinyin_cn --download`，会生成 `data/hanyupinyin_cn/pinyin_parts.json` 并下载 mp3 到前台 `public/sounds/pinyin-parts/`。
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
TTS_TIMEOUT_SECONDS=180
TTS_CONNECT_TIMEOUT_SECONDS=30
TTS_RECEIVE_TIMEOUT_SECONDS=120
TTS_RETRY_ATTEMPTS=3
TTS_RETRY_DELAY_SECONDS=2.0
TTS_BATCH_DELAY_SECONDS=0.2
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
- `word_match_word`（词语连连看整词）
- 词语导入/重试 TTS 时还会为每个单字生成 `pinyin_word_hanzi`（游戏格子小喇叭用）

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
