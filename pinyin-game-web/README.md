# 拼音练习 - 前台学习端

Vue 3 + Vite + TypeScript，移动端优先的儿童拼音配对游戏。

## 启动

```bash
npm install
npm run dev
```

默认 http://localhost:5173 。开发环境 API 为 `/api`，由 Vite 代理到 `http://127.0.0.1:8000`（见 `.env.development`）。

## 环境变量

| 文件 | 模式 | `VITE_API_BASE_URL` |
|------|------|---------------------|
| `.env.development` | `npm run dev` | `/api`（本地代理） |
| `.env.production` | `npm run build` | `https://game.beyondttyy.top/api` |
| `.env.local` | 覆盖上述配置（不提交 Git） | 自定义 |

生产构建：

```bash
npm run build
```

产物在 `dist/`，请求会直连生产 API。若临时指向其他地址，可在 `.env.local` 中设置 `VITE_API_BASE_URL` 后重新构建。

生产登录接口完整地址为 `https://game.beyondttyy.top/api/auth/login`（`baseURL` + `/auth/login`）。若服务器返回 404 且日志为 `POST /auth/login`，是 Nginx 反代剥掉了 `/api`，见 [docs/deployment.md](../docs/deployment.md) 与 `nginx/game.beyondttyy.top.conf`。

### 手机 / 局域网调试

开发服务器已配置 `host: true`，启动后终端会显示 **Network** 地址（形如 `http://192.168.x.x:5173`）。手机与电脑连同一 WiFi，用该地址在浏览器打开即可。

注意：

1. 需先在本机启动后端：`uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`（前台通过 Vite 代理 `/api`，手机无需直连 8000 端口）
2. Windows 防火墙若拦截，需允许 Node/Vite 的专用网络访问
3. 勿使用 `localhost`，手机应使用电脑的局域网 IP

## 音效

将以下文件放入 `public/sounds/`（可选）：

| 文件 | 用途 |
|------|------|
| `correct.mp3` | 配对成功（池化，支持连点） |
| `wrong.mp3` | 配对错误 |
| `select.mp3` | 选中卡片 |
| `click.mp3` | 按钮点击 |
| `start.mp3` | 开始练习 |
| `finish.mp3` | 提交完成 |

进入练习页会自动预加载。全部配对完成时有轻量撒花动画（可在系统设置中关闭动效）。

## 练习页布局（移动端）

默认 8 题共 16 张卡，棋盘为 **4 列 × 4 行**（含 iPhone 等窄屏）。卡片字号：汉字 20px、拼音 16px。题量少于 6 题时为 3 列。

## 登录与注册

访问 `/login`，可切换 **登录 / 注册**。注册成功后自动登录并进入练习册列表。

- 用户名 2–64 位，密码至少 6 位
- 注册账号角色固定为学生（`student`）

## 演示账号

student / student123
