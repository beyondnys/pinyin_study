-- 已有库增量：自适应掌握度表（与 wrong_questions 独立）
USE pinyin_game;

CREATE TABLE IF NOT EXISTS user_item_mastery (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,
  content_type VARCHAR(32) NOT NULL COMMENT 'pinyin_pair/word_choice/idiom_choice',
  content_id BIGINT NOT NULL,
  scope_type VARCHAR(32) NOT NULL,
  scope_id BIGINT NOT NULL,
  state VARCHAR(16) NOT NULL DEFAULT 'unseen',
  wrong_count INT NOT NULL DEFAULT 0,
  correct_streak INT NOT NULL DEFAULT 0,
  total_attempts INT NOT NULL DEFAULT 0,
  last_result TINYINT NULL,
  last_wrong_at DATETIME NULL,
  last_correct_at DATETIME NULL,
  last_practiced_at DATETIME NULL,
  next_review_at DATETIME NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT NOT NULL DEFAULT 0,
  UNIQUE KEY uk_user_content_scope (user_id, content_type, content_id, scope_type, scope_id, is_deleted),
  INDEX idx_user_scope (user_id, scope_type, scope_id),
  INDEX idx_user_review (user_id, next_review_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
