-- 拼音练习游戏：选声母/韵母/声调
-- 执行后运行：python -m app.scripts.sync_pinyin_questions

CREATE TABLE IF NOT EXISTS `pinyin_question` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `source_type` VARCHAR(32) DEFAULT NULL COMMENT '来源：practice_question / word_library',
  `source_id` BIGINT DEFAULT NULL COMMENT '来源表主键',
  `hanzi` VARCHAR(16) NOT NULL COMMENT '汉字（单字）',
  `initial` VARCHAR(16) NOT NULL DEFAULT '' COMMENT '声母，无声母为空串',
  `final` VARCHAR(32) NOT NULL COMMENT '韵母（不含声调数字）',
  `tone` TINYINT NOT NULL COMMENT '声调 1-4，轻声为 5',
  `pinyin_display` VARCHAR(64) NOT NULL COMMENT '带调完整拼音，如 zhōng',
  `status` TINYINT NOT NULL DEFAULT 1 COMMENT '1 启用 0 停用',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` BIGINT DEFAULT NULL,
  `updated_by` BIGINT DEFAULT NULL,
  `is_deleted` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_hanzi_active` (`hanzi`, `is_deleted`),
  KEY `idx_status` (`status`, `is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='拼音选拼题库';

CREATE TABLE IF NOT EXISTS `pinyin_game_record` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` BIGINT DEFAULT NULL COMMENT '未登录为空',
  `session_id` VARCHAR(64) DEFAULT NULL COMMENT '游客会话标识',
  `question_id` BIGINT NOT NULL COMMENT 'pinyin_question.id',
  `hanzi` VARCHAR(16) NOT NULL,
  `user_initial` VARCHAR(16) NOT NULL DEFAULT '',
  `user_final` VARCHAR(32) NOT NULL,
  `user_tone` TINYINT NOT NULL,
  `is_correct` TINYINT NOT NULL COMMENT '1 对 0 错',
  `duration_ms` INT NOT NULL DEFAULT 0 COMMENT '本题耗时毫秒',
  `score_delta` INT NOT NULL DEFAULT 0 COMMENT '本题得分变化',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` BIGINT DEFAULT NULL,
  `updated_by` BIGINT DEFAULT NULL,
  `is_deleted` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_user` (`user_id`),
  KEY `idx_session` (`session_id`),
  KEY `idx_question` (`question_id`),
  KEY `idx_created` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='拼音选拼答题记录';
