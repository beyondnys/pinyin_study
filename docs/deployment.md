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

前台与后台生产 API 均配置为 `https://game.beyondttyy.top/api`（见各自 `.env.production`）。开发时使用 `/api` + Vite 代理。

将 `dist` 分别部署到：

- `/var/www/pinyin-game/web`
- `/var/www/pinyin-game/admin`

### 4. Nginx

复制 `nginx/pinyin-game.conf` 或 `nginx/game.beyondttyy.top.conf` 到 `/etc/nginx/sites-available/` 并启用。

生产域名 `game.beyondttyy.top` 时，前端 `VITE_API_BASE_URL` 为 `https://game.beyondttyy.top/api`，浏览器请求示例：

`POST https://game.beyondttyy.top/api/auth/login`

后端 FastAPI 注册路径为 **`/api/auth/login`**（见 `app/main.py`）。

#### 登录 404：`POST /auth/login` 404 Not Found

若 Uvicorn 日志里是 `POST /auth/login` 而不是 `POST /api/auth/login`，说明 Nginx **剥掉了 `/api` 前缀**。请修改 `location /api/`：

```nginx
# 正确（保留完整 URI）
location /api/ {
    proxy_pass http://127.0.0.1:8006;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# 错误 — 不要这样写
# proxy_pass http://127.0.0.1:8006/;
```

改完后：`nginx -t && systemctl reload nginx`，再测登录。本机可直接验证：

```bash
curl -s -o /dev/null -w "%{http_code}" -X POST http://127.0.0.1:8006/api/auth/login \
  -H "Content-Type: application/json" -d '{"username":"x","password":"x"}'
```

应返回 `200` 或业务错误码 JSON，而不是 `404`。

### 5. 安全建议

- 修改 `JWT_SECRET`
- 修改默认管理员密码
- 配置 HTTPS（Certbot）
- 限制 CORS 为实际域名
