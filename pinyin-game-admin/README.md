# 拼音练习 - 管理后台

Vue 3 + Element Plus 管理端。

## 启动

```bash
npm install
npm run dev
```

访问 http://localhost:5174/admin/ 。开发环境 API 为 `/api`，由 Vite 代理到 `http://127.0.0.1:8066`（见 `.env.development`）。

默认账号：admin / admin123

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

产物在 `dist/`，部署到站点 `/admin/` 目录（与 `vite.config.ts` 中 `base: '/admin/'` 一致）。登录等请求示例：`https://game.beyondttyy.top/api/auth/login`。

若接口 404 且后端日志为 `POST /auth/login`（缺少 `/api` 前缀），请检查 Nginx `proxy_pass` 配置，见 [docs/deployment.md](../docs/deployment.md)。

## 练习册题目（拼音练练看）

- 单题添加
- **批量导入**：粘贴文本，自动提取汉字；本册已有、字库已有不重复导入

## 词语词库（词语连连看）

菜单：**词语连连看 → 词语词库**

- 新建词库 → 进入「词语」管理
- **批量导入词语**：每行一个 2～4 字词（如 `中国`、`自行车`）
- 自动生成拼音与整词 TTS

## 学习记录

菜单分为：

- **学习记录 → 拼音练习**：`practice_records`
- **学习记录 → 词语连连看**：`word_match_records`
