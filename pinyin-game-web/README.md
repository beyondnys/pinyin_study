# 拼音练习 - 前台学习端

Vue 3 + Vite + TypeScript，移动端优先的儿童拼音配对游戏。

## 启动

```bash
npm install
npm run dev
```

默认 http://localhost:5173 ，API 代理到 `http://127.0.0.1:8000`。

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

## 登录与注册

访问 `/login`，可切换 **登录 / 注册**。注册成功后自动登录并进入练习册列表。

- 用户名 2–64 位，密码至少 6 位
- 注册账号角色固定为学生（`student`）

## 演示账号

student / student123
