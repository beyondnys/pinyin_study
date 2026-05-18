# 拼音声调符号与多音字

## 存储格式

| 字段 | 说明 | 示例（「中」） |
|------|------|----------------|
| `pinyin` | 主读音，卡片展示与默认标准答案 | `zhōng` |
| `pinyin_list` | JSON 数组，全部合法读音 | `["zhōng","zhòng"]` |
| `pinyin_plain` | 无声调主音，检索用 | `zhong` |

生成逻辑：`app/services/pinyin_service.py`（`pypinyin` + `Style.TONE` + `heteronym=True`）。

## 判题

`app/utils/pinyin_util.is_pinyin_match`：用户提交的 `user_pinyin` 与主音或 `pinyin_list` 中任一项相同即判对（忽略大小写）。

## 迁移（已有 zhong1 数据）

```bash
mysql -u root -p pinyin_game < sql/migrate_pinyin_tone.sql
cd pinyin-game-api
python -m app.scripts.migrate_pinyin_to_tone --dry-run
python -m app.scripts.migrate_pinyin_to_tone
```

## 说明

- 练习页配对仍显示**主读音**一张拼音卡；多音字其它读法用于提交判题兼容。
- 多字词按逐字多音组合，最多 16 种组合（见 `MAX_PINYIN_VARIANTS`）。
- 管理端字库/题目 API 的 `pinyin_list` 为数组，便于展示全部读音。
