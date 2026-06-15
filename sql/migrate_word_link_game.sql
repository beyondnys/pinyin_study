-- 词语连连看：按顺序连字成词（2～4 字词，每字一卡）
-- 执行：mysql -u root -p pinyin_game < sql/migrate_word_link_game.sql

CREATE TABLE IF NOT EXISTS `word_books` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `title` VARCHAR(128) NOT NULL COMMENT '词库标题',
  `description` VARCHAR(512) NOT NULL DEFAULT '' COMMENT '词库描述',
  `question_count` INT NOT NULL DEFAULT 0 COMMENT '题目数量冗余',
  `status` TINYINT NOT NULL DEFAULT 1 COMMENT '1 启用 0 下架',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` BIGINT DEFAULT NULL,
  `updated_by` BIGINT DEFAULT NULL,
  `is_deleted` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_status` (`status`, `is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='词语连连看词库';

CREATE TABLE IF NOT EXISTS `word_questions` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `book_id` BIGINT NOT NULL COMMENT '所属词库 ID',
  `word` VARCHAR(16) NOT NULL COMMENT '完整词语，2～4 字',
  `pinyin` VARCHAR(128) NOT NULL DEFAULT '' COMMENT '整词拼音（带调）',
  `pinyin_list` VARCHAR(512) NOT NULL DEFAULT '[]' COMMENT '多音 JSON，预留',
  `word_len` TINYINT NOT NULL COMMENT '字数 2～4',
  `meaning` VARCHAR(256) DEFAULT NULL COMMENT '释义，预留对接外部 API',
  `sort_order` INT NOT NULL DEFAULT 0 COMMENT '册内排序',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` BIGINT DEFAULT NULL,
  `updated_by` BIGINT DEFAULT NULL,
  `is_deleted` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_book` (`book_id`, `is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='词语连连看题目';

CREATE TABLE IF NOT EXISTS `word_match_records` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` BIGINT NOT NULL COMMENT '学生用户 ID',
  `book_id` BIGINT NOT NULL COMMENT '词库 ID',
  `total_count` INT NOT NULL COMMENT '本轮词语总数',
  `correct_count` INT NOT NULL COMMENT '连对词语数',
  `accuracy` DECIMAL(5,2) NOT NULL COMMENT '正确率',
  `duration_seconds` INT NOT NULL DEFAULT 0 COMMENT '耗时秒',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` BIGINT DEFAULT NULL,
  `updated_by` BIGINT DEFAULT NULL,
  `is_deleted` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_user` (`user_id`, `is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='词语连连看练习记录';

CREATE TABLE IF NOT EXISTS `word_match_answer_details` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `record_id` BIGINT NOT NULL COMMENT '关联 word_match_records.id',
  `question_id` BIGINT NOT NULL COMMENT 'word_questions.id',
  `word` VARCHAR(16) NOT NULL COMMENT '词语快照',
  `is_correct` TINYINT NOT NULL COMMENT '1 连对 0 未完成或错',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` BIGINT DEFAULT NULL,
  `updated_by` BIGINT DEFAULT NULL,
  `is_deleted` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_record` (`record_id`, `is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='词语连连看答题明细';
