-- 拼音格式迁移：数字调 (zhong1) -> 声调符号 (zhōng)，并增加多音字列表字段
-- 执行后请运行：python -m app.scripts.migrate_pinyin_to_tone
USE pinyin_game;

ALTER TABLE word_libraries
  ADD COLUMN pinyin_list VARCHAR(512) NOT NULL DEFAULT '[]'
    COMMENT '全部读音 JSON，含多音字' AFTER pinyin;

ALTER TABLE practice_questions
  ADD COLUMN pinyin_list VARCHAR(512) NOT NULL DEFAULT '[]'
    COMMENT '全部合法读音 JSON' AFTER pinyin;

-- 更新字段注释（可选，MySQL 8+）
ALTER TABLE word_libraries
  MODIFY COLUMN pinyin VARCHAR(64) NOT NULL COMMENT '主读音（声调符号，如 zhōng）';

ALTER TABLE practice_questions
  MODIFY COLUMN pinyin VARCHAR(64) NOT NULL COMMENT '题目主读音（声调符号）';
