# API 规范

统一前缀：`/api`

## 响应格式

```json
{
  "code": 0,
  "message": "ok",
  "data": {}
}
```

`code != 0` 表示业务错误；HTTP 401/403 表示鉴权失败。

## 认证

请求头：`Authorization: Bearer {token}`

## 主要接口

### 认证

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /auth/login | 登录 |
| POST | /auth/register | 学生注册（成功后返回 token，同登录） |
| POST | /auth/logout | 退出 |
| GET | /auth/me | 当前用户 |

### 前台 /web

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /web/books | 练习册列表 |
| GET | /web/books/{id}/game | 游戏卡片 |
| POST | /web/practice/submit | 提交练习 |
| GET | /web/practice/records/{id} | 练习结果 |
| GET | /web/wrong-questions | 错题本 |
| POST | /web/wrong-questions/attempt | 配对选错时记入错题（即时，无需提交练习） |

### 游戏 /game/pinyin-select（拼音练习游戏，登录可选）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /game/pinyin-select/question/next | 随机下一题（不含答案），含 `zero_initial`（无声母时可直选韵母）；Query: session_id, exclude_ids |
| POST | /game/pinyin-select/answer | 提交声母/韵母/声调，后端判题 |
| GET | /game/pinyin-select/statistics | 统计，Query: session_id（游客必填） |
| GET | /game/pinyin-select/part-audio | 声母/韵母朗读，Query: text, kind=initial\|final |

### 后台 /admin

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /admin/dashboard/stats | 仪表盘统计 |
| CRUD | /admin/users | 用户 |
| CRUD | /admin/words | 字库 |
| CRUD | /admin/books | 练习册 |
| CRUD | /admin/books/{book_id}/questions | 题目 |
| POST | /admin/books/{book_id}/questions/batch-import | 练习册题目批量文本导入 |
| POST | /admin/import-tasks | 文本导入 |
| GET | /admin/import-tasks | 导入任务列表 |
| GET | /admin/practice-records | 学习记录 |
| GET | /admin/wrong-questions | 错题查询 |
