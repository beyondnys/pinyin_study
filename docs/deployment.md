# 部署指南

## 环境要求

- Python 3.10+
- Node.js 18+（仅构建前端）
- MySQL 8.x
- Redis 6+
- Nginx

## 构建步骤

### 1. 数据库

```bash
mysql -u root -p < sql/init.sql
cd pinyin-game-api && python -m app.scripts.init_admin
```

### 2. 后端

```bash
cd pinyin-game-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 生产配置
```

### systemd 示例

```ini
[Unit]
Description=Pinyin Game API
After=network.target mysql.service redis.service

[Service]
User=www-data
WorkingDirectory=/var/www/pinyin-game/api
EnvironmentFile=/var/www/pinyin-game/api/.env
ExecStart=/var/www/pinyin-game/api/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 2
Restart=always

[Install]
WantedBy=multi-user.target
```

### 3. 前端构建

```bash
cd pinyin-game-web && npm ci && npm run build
cd pinyin-game-admin && npm ci && npm run build
```

将 `dist` 分别部署到：

- `/var/www/pinyin-game/web`
- `/var/www/pinyin-game/admin`

### 4. Nginx

复制 `nginx/pinyin-game.conf` 到 `/etc/nginx/sites-available/` 并启用。

### 5. 安全建议

- 修改 `JWT_SECRET`
- 修改默认管理员密码
- 配置 HTTPS（Certbot）
- 限制 CORS 为实际域名
