# 拼音练习网页小游戏

儿童拼音练习系统：前台学习端 + 后台管理端 + FastAPI + MySQL + Redis。

## 项目结构

```
py_study/
├── pinyin-game-api/      # FastAPI 后端
├── pinyin-game-web/      # 前台学习端 (Vue3)
├── pinyin-game-admin/    # 后台管理端 (Vue3)
├── docs/                 # 设计文档
├── sql/init.sql          # 数据库初始化
└── nginx/pinyin-game.conf
```

## 快速启动（本地开发）

### 1. 数据库与 Redis

```bash
mysql -u root -p < sql/init.sql
redis-server
```

### 2. 后端

```bash
cd pinyin-game-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # 修改数据库与 Redis 连接
python -m app.scripts.init_admin
python -m app.scripts.seed_demo_data
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

默认管理员：`admin` / `admin123`  
演示学生：`student` / `student123`

### 5. 演示练习数据（列表为空时必做）

```bash
cd pinyin-game-api
source venv/bin/activate
python -m app.scripts.seed_demo_data
```

前台刷新后可见练习册列表，点击进入即可练习（按掌握度加权出题，错题优先）。

已有数据库需执行掌握度表迁移：`mysql ... pinyin_game < sql/init_learning.sql`（详见 [docs/learning_mastery.md](docs/learning_mastery.md)）。

拼音由数字调改为声调符号（如 zhōng）及多音字列表：`sql/migrate_pinyin_tone.sql` + `python -m app.scripts.migrate_pinyin_to_tone`（详见 [docs/pinyin_tone.md](docs/pinyin_tone.md)）。

### 3. 前台学习端

```bash
cd pinyin-game-web
npm install
npm run dev
```

访问 http://localhost:5173 ，可在登录页 **注册** 新学生账号或使用演示账号登录。

### 4. 后台管理端

```bash
cd pinyin-game-admin
npm install
npm run dev
```

访问 http://localhost:5174/admin/

## 生产部署

详见 [docs/deployment.md](docs/deployment.md)

## 技术栈

- 前端：Vue 3 + Vite + TypeScript + Element Plus + Pinia
- 后端：FastAPI + SQLAlchemy 2 + Redis + PyJWT + pypinyin
- 数据库：MySQL 8.x

## 文档

- [数据库设计](docs/database_design.md)
- [API 说明](docs/api_spec.md)
- [部署指南](docs/deployment.md)
