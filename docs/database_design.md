# 数据库设计

字段含义以 ORM 为准：`pinyin-game-api/app/models/*.py` 中 `mapped_column(..., comment="...")`。

## ER 关系简述

- `users`：管理员与学生
- `word_libraries`：汉字拼音字库
- `practice_books`：练习册
- `practice_questions`：练习册下的题目（汉字+拼音）
- `practice_records`：一次练习汇总
- `practice_answer_details`：每题答题明细
- `wrong_questions`：用户错题本（展示/运营，与掌握度独立）
- `user_item_mastery`：用户内容掌握度（加权抽题、streak、复习间隔）
- `import_tasks`：文本导入任务

## 统一审计字段（AuditMixin）

所有业务表均包含：

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT PK | 主键，自增 |
| created_at | DATETIME | 记录创建时间 |
| updated_at | DATETIME | 记录最后更新时间 |
| created_by | BIGINT NULL | 创建人用户 ID，系统脚本可为空 |
| updated_by | BIGINT NULL | 最后修改人用户 ID |
| is_deleted | TINYINT | 软删除：0 正常，1 已删除 |

---

## users

| 字段 | 说明 |
|------|------|
| username | 登录用户名，与 is_deleted 组合唯一 |
| password_hash | bcrypt 密码哈希，明文不落库 |
| nickname | 显示昵称 |
| role | admin 管理端 / student 学生端 |
| status | 1 启用，0 禁用 |

---

## word_libraries

| 字段 | 说明 |
|------|------|
| hanzi | 汉字，与 is_deleted 组合唯一 |
| pinyin | 带声调拼音，展示与判题用 |
| pinyin_plain | 无声调拼音，检索与比对用 |
| tone | 声调 1-4，轻声可为空 |
| remark | 备注说明 |

---

## practice_books

| 字段 | 说明 |
|------|------|
| title | 练习册标题 |
| description | 练习册描述 |
| question_count | 题目数量冗余，增删题时由业务维护 |
| status | 1 启用前台可见，0 下架 |

---

## practice_questions

| 字段 | 说明 |
|------|------|
| book_id | 所属练习册 ID |
| hanzi | 题目汉字 |
| pinyin | 题目标准拼音，带声调 |
| sort_order | 册内排序，越小越靠前 |

掌握度 `user_item_mastery.content_id` 在拼音场景下即本表 `id`。

---

## practice_records

| 字段 | 说明 |
|------|------|
| user_id | 练习学生用户 ID |
| book_id | 练习册 ID |
| total_count | 本次提交题目总数 |
| correct_count | 本次答对题数 |
| accuracy | 正确率百分比，如 87.50 |
| duration_seconds | 本次练习耗时（秒） |

---

## practice_answer_details

| 字段 | 说明 |
|------|------|
| record_id | 关联 practice_records.id |
| question_id | 题目 ID，对应 practice_questions.id |
| hanzi | 题目汉字快照 |
| user_pinyin | 用户提交的拼音 |
| correct_pinyin | 标准拼音快照 |
| is_correct | 1 对，0 错 |

---

## wrong_questions

与 `user_item_mastery` 独立，不参与加权抽题。

写入时机：配对游戏选错（`POST /api/web/wrong-questions/attempt`）；或练习提交时拼音判错（`POST /api/web/practice/submit` 中 `is_correct=0`）。

| 字段 | 说明 |
|------|------|
| user_id | 学生用户 ID |
| book_id | 关联练习册 ID |
| hanzi | 错题汉字 |
| pinyin | 正确拼音 |
| wrong_count | 累计答错次数 |
| last_wrong_at | 最近一次答错时间 |

---

## user_item_mastery

粒度：用户 + content_type + content_id + scope。

| 字段 | 说明 |
|------|------|
| user_id | 学生用户 ID |
| content_type | pinyin_pair / word_choice / idiom_choice 等 |
| content_id | 业务主键，拼音为 practice_questions.id |
| scope_type | 场景类型，如 book、global |
| scope_id | 场景 ID，如 book_id |
| state | unseen / learning / mastered |
| wrong_count | 历史累计答错次数 |
| correct_streak | 当前连续答对次数，答错清零 |
| total_attempts | 累计作答次数 |
| last_result | 最近一次：1 对，0 错 |
| last_wrong_at | 最近一次答错时间 |
| last_correct_at | 最近一次答对时间 |
| last_practiced_at | 最近一次练习时间 |
| next_review_at | 下次建议复习时间，到期后抽题权重升高 |

详见 [learning_mastery.md](learning_mastery.md)。

---

## import_tasks

| 字段 | 说明 |
|------|------|
| title | 任务名称 |
| raw_text | 待导入原始文本 |
| book_id | 目标练习册 ID，可为空 |
| status | pending / processing / done / failed |
| result_message | 执行结果说明 |

---

## Redis Key

| Key | 说明 | TTL |
|-----|------|-----|
| `login:token:{token}` | 会话 JSON | 7 天 |
| `user:tokens:{user_id}` | 用户 token 集合 | 随 token |
