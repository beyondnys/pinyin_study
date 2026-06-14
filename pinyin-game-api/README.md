# Pinyin Game API

FastAPI 后端服务。

## 环境

- **推荐 Python 3.11 或 3.12**（规格要求 3.10+）
- 若使用 **Python 3.9**：Pydantic 模型与 SQLAlchemy 须写 `Optional[str]`，勿用 `str | None`；建议尽快升级到 3.10+

## 启动

```bash
python3.12 -m venv .venv   # 或 venv，请保证 >=3.10
source .venv/bin/activate
pip install -r requirements.txt
# 密码使用 bcrypt（已移除 passlib，避免与 bcrypt 5.x / Python 3.13 不兼容）
cp .env.example .env
# 务必在 .env 中配置数据库（会覆盖 config.py 里的默认值）
python -m app.scripts.init_admin
python -m app.scripts.seed_demo_data
uvicorn app.main:app --reload --port 8000
```

API 文档：http://127.0.0.1:8000/docs

## 脚本

### 创建管理员（admin / admin123）

先确保已执行 `sql/init.sql` 且 `.env` 数据库配置正确，再运行：

```bash
cd pinyin-game-api
source venv/bin/activate
python -m app.scripts.init_admin
```

或：

```bash
chmod +x scripts/create_admin.sh
./scripts/create_admin.sh
```

自定义账号：

```bash
python -m app.scripts.init_admin -u admin -p 你的密码
python -m app.scripts.init_admin --reset   # 已存在时重置密码
```

### 演示数据

- `python -m app.scripts.seed_demo_data` — 学生 student/student123 + 示例练习册

### 拼音格式迁移（zhong1 → zhōng + 多音字）

已有库从数字调升级为**声调符号**，并填充 `pinyin_list` 多音字列表：

```bash
mysql -u root -p pinyin_game < ../sql/migrate_pinyin_tone.sql
python -m app.scripts.migrate_pinyin_to_tone --dry-run   # 预览
python -m app.scripts.migrate_pinyin_to_tone             # 写入
```

新导入/字库生成均使用 `Style.TONE`；判题时 `user_pinyin` 命中主音或 `pinyin_list` 中任一读法均算正确。

### 拼音练习游戏

```bash
mysql -u root -p pinyin_game < ../sql/migrate_pinyin_select_game.sql
python -m app.scripts.sync_pinyin_questions
```

接口前缀：`/api/game/pinyin-select`（见 [docs/api_spec.md](../docs/api_spec.md)）。

**排查**：前台点击声母/韵母顶部出现 `Not Found`，多为本机 `uvicorn` 未加载新路由。请用 `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` 重启；可访问 `http://127.0.0.1:8000/docs` 确认是否存在 `GET /api/game/pinyin-select/part-audio`。

声母/韵母朗读优先使用 [hanyupinyin.cn](http://www.hanyupinyin.cn/) 标准 mp3（抓取脚本见下），无本地文件时用汉语认读字 TTS（`app/utils/pinyin_part_tts_util.py`）。

```bash
python -m app.scripts.scrape_hanyupinyin_cn --download
```

会写入 `data/hanyupinyin_cn/pinyin_parts.json`，并将 mp3 同步到 `pinyin-game-web/public/sounds/pinyin-parts/`。

### TTS 语音（edge-tts + MinIO）

详见 [docs/tts.md](../docs/tts.md)。迁移表：`sql/migrate_tts_audio.sql`；回填：`python -m app.scripts.backfill_tts_audio`。

## Windows 发布打包

在项目根目录双击或执行：

```bat
build.bat
```

（`build.bat` 会调用同目录的 `build.ps1` 生成 zip，避免 bat 内多行 PowerShell 在 cmd 下被拆行报错。）

会在 `dist` 目录生成 **`yyyyMMddHHmmss.zip` 压缩包**（不是解压后的文件夹；例如 `20250517143022.zip`），包含：

- `app/`（不含 `__pycache__`）
- `scripts/`
- `requirements.txt`、`.env.example`、`README.md`

不包含 `.env`、虚拟环境等敏感或本地文件。解压后按脚本末尾提示配置 `.env` 并安装依赖后启动。
