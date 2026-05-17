# Pinyin Game API

FastAPI 后端服务。

## 环境

- **推荐 Python 3.11 或 3.12**（规格要求 3.10+）
- 若使用 **Python 3.9**，项目已加 `from __future__ import annotations` 兼容，但建议尽快升级

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
