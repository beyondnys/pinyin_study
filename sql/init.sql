-- 拼音练习系统 - MySQL 初始化脚本
CREATE DATABASE IF NOT EXISTS pinyin_game DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE pinyin_game;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(64) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  nickname VARCHAR(64) DEFAULT '',
  role ENUM('admin','student') NOT NULL DEFAULT 'student',
  status TINYINT NOT NULL DEFAULT 1 COMMENT '1启用 0禁用',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT NOT NULL DEFAULT 0,
  UNIQUE KEY uk_username (username, is_deleted),
  INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 字库表
CREATE TABLE IF NOT EXISTS word_libraries (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  hanzi VARCHAR(16) NOT NULL,
  pinyin VARCHAR(64) NOT NULL COMMENT '带声调',
  pinyin_plain VARCHAR(64) NOT NULL COMMENT '无声调',
  tone TINYINT NULL,
  remark VARCHAR(255) DEFAULT '',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT NOT NULL DEFAULT 0,
  UNIQUE KEY uk_hanzi (hanzi, is_deleted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 练习册表
CREATE TABLE IF NOT EXISTS practice_books (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(128) NOT NULL,
  description VARCHAR(512) DEFAULT '',
  question_count INT NOT NULL DEFAULT 0,
  status TINYINT NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 题目表
CREATE TABLE IF NOT EXISTS practice_questions (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  book_id BIGINT NOT NULL,
  hanzi VARCHAR(16) NOT NULL,
  pinyin VARCHAR(64) NOT NULL,
  sort_order INT NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT NOT NULL DEFAULT 0,
  INDEX idx_book (book_id),
  CONSTRAINT fk_question_book FOREIGN KEY (book_id) REFERENCES practice_books(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 学习记录表
CREATE TABLE IF NOT EXISTS practice_records (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,
  book_id BIGINT NOT NULL,
  total_count INT NOT NULL,
  correct_count INT NOT NULL,
  accuracy DECIMAL(5,2) NOT NULL,
  duration_seconds INT NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT NOT NULL DEFAULT 0,
  INDEX idx_user_book (user_id, book_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 答题明细表
CREATE TABLE IF NOT EXISTS practice_answer_details (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  record_id BIGINT NOT NULL,
  question_id BIGINT NOT NULL,
  hanzi VARCHAR(16) NOT NULL,
  user_pinyin VARCHAR(64) NOT NULL,
  correct_pinyin VARCHAR(64) NOT NULL,
  is_correct TINYINT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT NOT NULL DEFAULT 0,
  INDEX idx_record (record_id),
  CONSTRAINT fk_detail_record FOREIGN KEY (record_id) REFERENCES practice_records(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户内容掌握度（自适应抽题，与错题本独立）
CREATE TABLE IF NOT EXISTS user_item_mastery (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,
  content_type VARCHAR(32) NOT NULL COMMENT 'pinyin_pair/word_choice/idiom_choice',
  content_id BIGINT NOT NULL COMMENT '业务表主键，如 practice_questions.id',
  scope_type VARCHAR(32) NOT NULL COMMENT 'book/global 等',
  scope_id BIGINT NOT NULL COMMENT '如 book_id',
  state VARCHAR(16) NOT NULL DEFAULT 'unseen' COMMENT 'unseen/learning/mastered',
  wrong_count INT NOT NULL DEFAULT 0,
  correct_streak INT NOT NULL DEFAULT 0,
  total_attempts INT NOT NULL DEFAULT 0,
  last_result TINYINT NULL COMMENT '0错 1对',
  last_wrong_at DATETIME NULL,
  last_correct_at DATETIME NULL,
  last_practiced_at DATETIME NULL,
  next_review_at DATETIME NULL COMMENT '复习间隔到期时间',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT NOT NULL DEFAULT 0,
  UNIQUE KEY uk_user_content_scope (user_id, content_type, content_id, scope_type, scope_id, is_deleted),
  INDEX idx_user_scope (user_id, scope_type, scope_id),
  INDEX idx_user_review (user_id, next_review_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 错题本表
CREATE TABLE IF NOT EXISTS wrong_questions (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,
  book_id BIGINT NOT NULL,
  hanzi VARCHAR(16) NOT NULL,
  pinyin VARCHAR(64) NOT NULL,
  wrong_count INT NOT NULL DEFAULT 1,
  last_wrong_at DATETIME NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT NOT NULL DEFAULT 0,
  UNIQUE KEY uk_user_hanzi (user_id, hanzi, is_deleted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 导入任务表
CREATE TABLE IF NOT EXISTS import_tasks (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(128) NOT NULL,
  raw_text TEXT NOT NULL,
  book_id BIGINT NULL,
  status ENUM('pending','processing','done','failed') NOT NULL DEFAULT 'pending',
  result_message VARCHAR(512) DEFAULT '',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT NULL,
  updated_by BIGINT NULL,
  is_deleted TINYINT NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
