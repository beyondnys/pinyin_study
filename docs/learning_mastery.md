# 自适应掌握度模块

与 **错题本 `wrong_questions`** 独立：错题本面向展示与运营；掌握度表面向 **加权抽题** 与 **复习间隔**。

## 粒度

`user_id` + `content_type` + `content_id` + `scope_type` + `scope_id`

- 拼音配对：`content_type=pinyin_pair`，`content_id=practice_questions.id`，`scope_type=book`，`scope_id=练习册 id`
- 后续词语/成语：新增 `ContentType` 与 `providers/` 即可

## 权重规则（见 `app/learning/config.py`）

| 状态 | 抽样倾向 |
|------|----------|
| 未做过 | 中等 `W_UNSEEN` |
| 学习中（含每次答错累加） | 高 `W_LEARNING`，错越多越高，24h 内再错额外加权 |
| 已掌握且未到 `next_review_at` | 低，但不低于 `W_FLOOR` |
| 已掌握且已到复习日 | 提升为 `W_DUE_REVIEW` |

## Streak 与间隔

- 每次 **答错**：`wrong_count++`，`correct_streak=0`，`next_review_at=now`（立即优先）
- 每次 **答对**：`correct_streak++`，按 `REVIEW_INTERVALS_DAYS` 设置下次复习时间
- 连续答对 **2** 次 → `state=mastered`

## 代码入口

| 能力 | 位置 |
|------|------|
| 加权抽题 | `LearningMasteryService.pick_pinyin_book_questions` |
| 记录作答 | `LearningMasteryService.record_pinyin_attempt` |
| 纯逻辑 | `mastery_engine.py`、`sampler.py` |

练习流程接入：

- `GET /web/books/{id}/game` → `build_game_data(..., user_id)`
- `POST /web/practice/submit` → 每题调用 `record_pinyin_attempt`（仍同步写错题本）

## 已有库迁移

```bash
mysql -u root -p pinyin_game < sql/init_learning.sql
```

## 扩展新题型

1. 在 `ContentType` 增加枚举  
2. 新增 `providers/xxx_provider.py` 返回 `CandidateItem` 列表  
3. 在 `LearningMasteryService` 增加 `pick_xxx` / `record_xxx_attempt`
