/*
 Navicat Premium Data Transfer

 Source Server         : 127.0.0.1-pinyin_game
 Source Server Type    : MySQL
 Source Server Version : 50728 (5.7.28)
 Source Host           : 127.0.0.1:3306
 Source Schema         : pinyin_game

 Target Server Type    : MySQL
 Target Server Version : 50728 (5.7.28)
 File Encoding         : 65001

 Date: 17/05/2026 21:19:59
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for import_tasks
-- ----------------------------
DROP TABLE IF EXISTS `import_tasks`;
CREATE TABLE `import_tasks` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL,
  `raw_text` text NOT NULL,
  `book_id` bigint(20) DEFAULT NULL,
  `status` enum('pending','processing','done','failed') NOT NULL DEFAULT 'pending',
  `result_message` varchar(512) DEFAULT '',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` bigint(20) DEFAULT NULL,
  `updated_by` bigint(20) DEFAULT NULL,
  `is_deleted` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of import_tasks
-- ----------------------------
BEGIN;
INSERT INTO `import_tasks` (`id`, `title`, `raw_text`, `book_id`, `status`, `result_message`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (1, '一级', '一、二、三、四、五、六、七、八、九、十\n人、口、手、足、头、耳、目、鼻、舌、牙\n山、水、火、土、金、木、日、月、星、云\n雨、雪、风、雷、电、气、天、地、中、国', 2, 'done', '成功导入 40 个汉字', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
COMMIT;

-- ----------------------------
-- Table structure for practice_answer_details
-- ----------------------------
DROP TABLE IF EXISTS `practice_answer_details`;
CREATE TABLE `practice_answer_details` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `record_id` bigint(20) NOT NULL,
  `question_id` bigint(20) NOT NULL,
  `hanzi` varchar(16) NOT NULL,
  `user_pinyin` varchar(64) NOT NULL,
  `correct_pinyin` varchar(64) NOT NULL,
  `is_correct` tinyint(4) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` bigint(20) DEFAULT NULL,
  `updated_by` bigint(20) DEFAULT NULL,
  `is_deleted` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_record` (`record_id`),
  CONSTRAINT `fk_detail_record` FOREIGN KEY (`record_id`) REFERENCES `practice_records` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of practice_answer_details
-- ----------------------------
BEGIN;
INSERT INTO `practice_answer_details` (`id`, `record_id`, `question_id`, `hanzi`, `user_pinyin`, `correct_pinyin`, `is_correct`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (1, 1, 6, '六', 'liu4', 'liu4', 1, '2026-05-17 11:58:06', '2026-05-17 11:58:06', 1, 1, 0);
INSERT INTO `practice_answer_details` (`id`, `record_id`, `question_id`, `hanzi`, `user_pinyin`, `correct_pinyin`, `is_correct`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (2, 1, 13, '手', 'shou3', 'shou3', 1, '2026-05-17 11:58:06', '2026-05-17 11:58:06', 1, 1, 0);
INSERT INTO `practice_answer_details` (`id`, `record_id`, `question_id`, `hanzi`, `user_pinyin`, `correct_pinyin`, `is_correct`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (3, 1, 21, '山', 'shan1', 'shan1', 1, '2026-05-17 11:58:06', '2026-05-17 11:58:06', 1, 1, 0);
INSERT INTO `practice_answer_details` (`id`, `record_id`, `question_id`, `hanzi`, `user_pinyin`, `correct_pinyin`, `is_correct`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (4, 1, 22, '水', 'shui3', 'shui3', 1, '2026-05-17 11:58:06', '2026-05-17 11:58:06', 1, 1, 0);
INSERT INTO `practice_answer_details` (`id`, `record_id`, `question_id`, `hanzi`, `user_pinyin`, `correct_pinyin`, `is_correct`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (5, 1, 35, '电', 'dian4', 'dian4', 1, '2026-05-17 11:58:06', '2026-05-17 11:58:06', 1, 1, 0);
INSERT INTO `practice_answer_details` (`id`, `record_id`, `question_id`, `hanzi`, `user_pinyin`, `correct_pinyin`, `is_correct`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (6, 1, 9, '九', 'jiu3', 'jiu3', 1, '2026-05-17 11:58:06', '2026-05-17 11:58:06', 1, 1, 0);
INSERT INTO `practice_answer_details` (`id`, `record_id`, `question_id`, `hanzi`, `user_pinyin`, `correct_pinyin`, `is_correct`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (7, 1, 4, '四', 'si4', 'si4', 1, '2026-05-17 11:58:06', '2026-05-17 11:58:06', 1, 1, 0);
INSERT INTO `practice_answer_details` (`id`, `record_id`, `question_id`, `hanzi`, `user_pinyin`, `correct_pinyin`, `is_correct`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (8, 1, 30, '云', 'yun2', 'yun2', 1, '2026-05-17 11:58:06', '2026-05-17 11:58:06', 1, 1, 0);
INSERT INTO `practice_answer_details` (`id`, `record_id`, `question_id`, `hanzi`, `user_pinyin`, `correct_pinyin`, `is_correct`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (9, 2, 51, '花', 'hua1', 'hua1', 1, '2026-05-17 12:41:23', '2026-05-17 12:41:23', 1, 1, 0);
INSERT INTO `practice_answer_details` (`id`, `record_id`, `question_id`, `hanzi`, `user_pinyin`, `correct_pinyin`, `is_correct`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (10, 2, 117, '丑', 'chou3', 'chou3', 1, '2026-05-17 12:41:23', '2026-05-17 12:41:23', 1, 1, 0);
INSERT INTO `practice_answer_details` (`id`, `record_id`, `question_id`, `hanzi`, `user_pinyin`, `correct_pinyin`, `is_correct`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (11, 2, 116, '美', 'mei3', 'mei3', 1, '2026-05-17 12:41:23', '2026-05-17 12:41:23', 1, 1, 0);
INSERT INTO `practice_answer_details` (`id`, `record_id`, `question_id`, `hanzi`, `user_pinyin`, `correct_pinyin`, `is_correct`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (12, 2, 149, '程', 'cheng2', 'cheng2', 1, '2026-05-17 12:41:23', '2026-05-17 12:41:23', 1, 1, 0);
INSERT INTO `practice_answer_details` (`id`, `record_id`, `question_id`, `hanzi`, `user_pinyin`, `correct_pinyin`, `is_correct`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (13, 2, 65, '桌', 'zhuo1', 'zhuo1', 1, '2026-05-17 12:41:23', '2026-05-17 12:41:23', 1, 1, 0);
INSERT INTO `practice_answer_details` (`id`, `record_id`, `question_id`, `hanzi`, `user_pinyin`, `correct_pinyin`, `is_correct`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (14, 2, 63, '行', 'xing2', 'xing2', 1, '2026-05-17 12:41:23', '2026-05-17 12:41:23', 1, 1, 0);
INSERT INTO `practice_answer_details` (`id`, `record_id`, `question_id`, `hanzi`, `user_pinyin`, `correct_pinyin`, `is_correct`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (15, 2, 115, '瘦', 'shou4', 'shou4', 1, '2026-05-17 12:41:23', '2026-05-17 12:41:23', 1, 1, 0);
INSERT INTO `practice_answer_details` (`id`, `record_id`, `question_id`, `hanzi`, `user_pinyin`, `correct_pinyin`, `is_correct`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (16, 2, 6, '六', 'liu4', 'liu4', 1, '2026-05-17 12:41:23', '2026-05-17 12:41:23', 1, 1, 0);
COMMIT;

-- ----------------------------
-- Table structure for practice_books
-- ----------------------------
DROP TABLE IF EXISTS `practice_books`;
CREATE TABLE `practice_books` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL,
  `description` varchar(512) DEFAULT '',
  `question_count` int(11) NOT NULL DEFAULT '0',
  `status` tinyint(4) NOT NULL DEFAULT '1',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` bigint(20) DEFAULT NULL,
  `updated_by` bigint(20) DEFAULT NULL,
  `is_deleted` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of practice_books
-- ----------------------------
BEGIN;
INSERT INTO `practice_books` (`id`, `title`, `description`, `question_count`, `status`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (1, '一年级', '', 0, 1, '2026-05-17 02:55:04', '2026-05-17 12:03:59', 1, 1, 1);
INSERT INTO `practice_books` (`id`, `title`, `description`, `question_count`, `status`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (2, '一年级', '由导入任务「一级」自动生成', 174, 1, '2026-05-17 02:58:02', '2026-05-17 12:16:18', 1, 1, 0);
COMMIT;

-- ----------------------------
-- Table structure for practice_questions
-- ----------------------------
DROP TABLE IF EXISTS `practice_questions`;
CREATE TABLE `practice_questions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `book_id` bigint(20) NOT NULL,
  `hanzi` varchar(16) NOT NULL,
  `pinyin` varchar(64) NOT NULL,
  `sort_order` int(11) NOT NULL DEFAULT '0',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` bigint(20) DEFAULT NULL,
  `updated_by` bigint(20) DEFAULT NULL,
  `is_deleted` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_book` (`book_id`),
  CONSTRAINT `fk_question_book` FOREIGN KEY (`book_id`) REFERENCES `practice_books` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=175 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of practice_questions
-- ----------------------------
BEGIN;
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (1, 2, '一', 'yi1', 0, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (2, 2, '二', 'er4', 1, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (3, 2, '三', 'san1', 2, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (4, 2, '四', 'si4', 3, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (5, 2, '五', 'wu3', 4, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (6, 2, '六', 'liu4', 5, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (7, 2, '七', 'qi1', 6, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (8, 2, '八', 'ba1', 7, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (9, 2, '九', 'jiu3', 8, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (10, 2, '十', 'shi2', 9, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (11, 2, '人', 'ren2', 10, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (12, 2, '口', 'kou3', 11, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (13, 2, '手', 'shou3', 12, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (14, 2, '足', 'zu2', 13, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (15, 2, '头', 'tou2', 14, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (16, 2, '耳', 'er3', 15, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (17, 2, '目', 'mu4', 16, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (18, 2, '鼻', 'bi2', 17, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (19, 2, '舌', 'she2', 18, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (20, 2, '牙', 'ya2', 19, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (21, 2, '山', 'shan1', 20, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (22, 2, '水', 'shui3', 21, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (23, 2, '火', 'huo3', 22, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (24, 2, '土', 'tu3', 23, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (25, 2, '金', 'jin1', 24, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (26, 2, '木', 'mu4', 25, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (27, 2, '日', 'ri4', 26, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (28, 2, '月', 'yue4', 27, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (29, 2, '星', 'xing1', 28, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (30, 2, '云', 'yun2', 29, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (31, 2, '雨', 'yu3', 30, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (32, 2, '雪', 'xue3', 31, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (33, 2, '风', 'feng1', 32, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (34, 2, '雷', 'lei2', 33, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (35, 2, '电', 'dian4', 34, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (36, 2, '气', 'qi4', 35, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (37, 2, '天', 'tian1', 36, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (38, 2, '地', 'di4', 37, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (39, 2, '中', 'zhong1', 38, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (40, 2, '国', 'guo2', 39, '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (41, 2, '猫', 'mao1', 40, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (42, 2, '狗', 'gou3', 41, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (43, 2, '猪', 'zhu1', 42, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (44, 2, '牛', 'niu2', 43, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (45, 2, '羊', 'yang2', 44, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (46, 2, '马', 'ma3', 45, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (47, 2, '鸡', 'ji1', 46, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (48, 2, '鸭', 'ya1', 47, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (49, 2, '鱼', 'yu2', 48, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (50, 2, '鸟', 'niao3', 49, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (51, 2, '花', 'hua1', 50, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (52, 2, '草', 'cao3', 51, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (53, 2, '树', 'shu4', 52, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (54, 2, '叶', 'ye4', 53, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (55, 2, '果', 'guo3', 54, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (56, 2, '瓜', 'gua1', 55, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (57, 2, '菜', 'cai4', 56, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (58, 2, '豆', 'dou4', 57, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (59, 2, '米', 'mi3', 58, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (60, 2, '衣', 'yi1', 59, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (61, 2, '食', 'shi2', 60, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (62, 2, '住', 'zhu4', 61, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (63, 2, '行', 'xing2', 62, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (64, 2, '床', 'chuang2', 63, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (65, 2, '桌', 'zhuo1', 64, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (66, 2, '椅', 'yi3', 65, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (67, 2, '灯', 'deng1', 66, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (68, 2, '杯', 'bei1', 67, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (69, 2, '碗', 'wan3', 68, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (70, 2, '车', 'che1', 69, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (71, 2, '船', 'chuan2', 70, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (72, 2, '飞', 'fei1', 71, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (73, 2, '机', 'ji1', 72, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (74, 2, '自', 'zi4', 73, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (75, 2, '摩', 'mo2', 74, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (76, 2, '托', 'tuo1', 75, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (77, 2, '百', 'bai3', 76, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (78, 2, '千', 'qian1', 77, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (79, 2, '万', 'wan4', 78, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (80, 2, '亿', 'yi4', 79, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (81, 2, '零', 'ling2', 80, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (82, 2, '个', 'ge4', 81, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (83, 2, '只', 'zhi3', 82, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (84, 2, '条', 'tiao2', 83, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (85, 2, '把', 'ba3', 84, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (86, 2, '本', 'ben3', 85, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (87, 2, '张', 'zhang1', 86, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (88, 2, '匹', 'pi3', 87, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (89, 2, '件', 'jian4', 88, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (90, 2, '心', 'xin1', 89, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (91, 2, '肝', 'gan1', 90, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (92, 2, '脾', 'pi2', 91, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (93, 2, '肺', 'fei4', 92, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (94, 2, '肾', 'shen4', 93, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (95, 2, '脚', 'jiao3', 94, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (96, 2, '指', 'zhi3', 95, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (97, 2, '掌', 'zhang3', 96, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (98, 2, '跑', 'pao3', 97, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (99, 2, '跳', 'tiao4', 98, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (100, 2, '走', 'zou3', 99, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (101, 2, '坐', 'zuo4', 100, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (102, 2, '立', 'li4', 101, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (103, 2, '卧', 'wo4', 102, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (104, 2, '吃', 'chi1', 103, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (105, 2, '喝', 'he1', 104, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (106, 2, '看', 'kan4', 105, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (107, 2, '听', 'ting1', 106, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (108, 2, '大', 'da4', 107, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (109, 2, '小', 'xiao3', 108, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (110, 2, '多', 'duo1', 109, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (111, 2, '少', 'shao3', 110, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (112, 2, '高', 'gao1', 111, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (113, 2, '矮', 'ai3', 112, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (114, 2, '胖', 'pang4', 113, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (115, 2, '瘦', 'shou4', 114, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (116, 2, '美', 'mei3', 115, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (117, 2, '丑', 'chou3', 116, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (118, 2, '快', 'kuai4', 117, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (119, 2, '慢', 'man4', 118, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (120, 2, '好', 'hao3', 119, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (121, 2, '坏', 'huai4', 120, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (122, 2, '早', 'zao3', 121, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (123, 2, '晚', 'wan3', 122, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (124, 2, '远', 'yuan3', 123, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (125, 2, '近', 'jin4', 124, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (126, 2, '真', 'zhen1', 125, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (127, 2, '假', 'jia3', 126, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (128, 2, '工', 'gong1', 127, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (129, 2, '厂', 'chang3', 128, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (130, 2, '作', 'zuo4', 129, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (131, 2, '长', 'zhang3', 130, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (132, 2, '房', 'fang2', 131, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (133, 2, '家', 'jia1', 132, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (134, 2, '上', 'shang4', 133, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (135, 2, '学', 'xue2', 134, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (136, 2, '升', 'sheng1', 135, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (137, 2, '面', 'mian4', 136, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (138, 2, '下', 'xia4', 137, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (139, 2, '降', 'jiang4', 138, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (140, 2, '左', 'zuo3', 139, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (141, 2, '边', 'bian1', 140, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (142, 2, '转', 'zhuan3', 141, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (143, 2, '右', 'you4', 142, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (144, 2, '前', 'qian2', 143, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (145, 2, '进', 'jin4', 144, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (146, 2, '后', 'hou4', 145, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (147, 2, '退', 'tui4', 146, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (148, 2, '里', 'li3', 147, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (149, 2, '程', 'cheng2', 148, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (150, 2, '外', 'wai4', 149, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (151, 2, '出', 'chu1', 150, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (152, 2, '东', 'dong1', 151, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (153, 2, '方', 'fang1', 152, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (154, 2, '南', 'nan2', 153, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (155, 2, '西', 'xi1', 154, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (156, 2, '北', 'bei3', 155, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (157, 2, '京', 'jing1', 156, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (158, 2, '庭', 'ting2', 157, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (159, 2, '回', 'hui2', 158, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (160, 2, '习', 'xi2', 159, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (161, 2, '校', 'xiao4', 160, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (162, 2, '生', 'sheng1', 161, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (163, 2, '园', 'yuan2', 162, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (164, 2, '爱', 'ai4', 163, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (165, 2, '情', 'qing2', 164, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (166, 2, '事', 'shi4', 165, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (167, 2, '朋', 'peng2', 166, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (168, 2, '友', 'you3', 167, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (169, 2, '亲', 'qin1', 168, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (170, 2, '辈', 'bei4', 169, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (171, 2, '谊', 'yi4', 170, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (172, 2, '认', 'ren4', 171, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (173, 2, '识', 'shi2', 172, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `practice_questions` (`id`, `book_id`, `hanzi`, `pinyin`, `sort_order`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (174, 2, '为', 'wei4', 173, '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
COMMIT;

-- ----------------------------
-- Table structure for practice_records
-- ----------------------------
DROP TABLE IF EXISTS `practice_records`;
CREATE TABLE `practice_records` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `book_id` bigint(20) NOT NULL,
  `total_count` int(11) NOT NULL,
  `correct_count` int(11) NOT NULL,
  `accuracy` decimal(5,2) NOT NULL,
  `duration_seconds` int(11) NOT NULL DEFAULT '0',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` bigint(20) DEFAULT NULL,
  `updated_by` bigint(20) DEFAULT NULL,
  `is_deleted` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_user_book` (`user_id`,`book_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of practice_records
-- ----------------------------
BEGIN;
INSERT INTO `practice_records` (`id`, `user_id`, `book_id`, `total_count`, `correct_count`, `accuracy`, `duration_seconds`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (1, 1, 2, 8, 8, 100.00, 46, '2026-05-17 11:58:06', '2026-05-17 11:58:06', 1, 1, 0);
INSERT INTO `practice_records` (`id`, `user_id`, `book_id`, `total_count`, `correct_count`, `accuracy`, `duration_seconds`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (2, 1, 2, 8, 8, 100.00, 27, '2026-05-17 12:41:23', '2026-05-17 12:41:23', 1, 1, 0);
COMMIT;

-- ----------------------------
-- Table structure for user_item_mastery
-- ----------------------------
DROP TABLE IF EXISTS `user_item_mastery`;
CREATE TABLE `user_item_mastery` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `content_type` varchar(32) NOT NULL COMMENT 'pinyin_pair/word_choice/idiom_choice',
  `content_id` bigint(20) NOT NULL,
  `scope_type` varchar(32) NOT NULL,
  `scope_id` bigint(20) NOT NULL,
  `state` varchar(16) NOT NULL DEFAULT 'unseen',
  `wrong_count` int(11) NOT NULL DEFAULT '0',
  `correct_streak` int(11) NOT NULL DEFAULT '0',
  `total_attempts` int(11) NOT NULL DEFAULT '0',
  `last_result` tinyint(4) DEFAULT NULL,
  `last_wrong_at` datetime DEFAULT NULL,
  `last_correct_at` datetime DEFAULT NULL,
  `last_practiced_at` datetime DEFAULT NULL,
  `next_review_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` bigint(20) DEFAULT NULL,
  `updated_by` bigint(20) DEFAULT NULL,
  `is_deleted` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_content_scope` (`user_id`,`content_type`,`content_id`,`scope_type`,`scope_id`,`is_deleted`),
  KEY `idx_user_scope` (`user_id`,`scope_type`,`scope_id`),
  KEY `idx_user_review` (`user_id`,`next_review_at`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of user_item_mastery
-- ----------------------------
BEGIN;
INSERT INTO `user_item_mastery` (`id`, `user_id`, `content_type`, `content_id`, `scope_type`, `scope_id`, `state`, `wrong_count`, `correct_streak`, `total_attempts`, `last_result`, `last_wrong_at`, `last_correct_at`, `last_practiced_at`, `next_review_at`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (1, 1, 'pinyin_pair', 51, 'book', 2, 'learning', 0, 1, 1, 1, NULL, '2026-05-17 04:41:24', '2026-05-17 04:41:24', '2026-05-17 04:41:24', '2026-05-17 12:41:23', '2026-05-17 12:41:23', 1, 1, 0);
INSERT INTO `user_item_mastery` (`id`, `user_id`, `content_type`, `content_id`, `scope_type`, `scope_id`, `state`, `wrong_count`, `correct_streak`, `total_attempts`, `last_result`, `last_wrong_at`, `last_correct_at`, `last_practiced_at`, `next_review_at`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (2, 1, 'pinyin_pair', 117, 'book', 2, 'learning', 0, 1, 1, 1, NULL, '2026-05-17 04:41:24', '2026-05-17 04:41:24', '2026-05-17 04:41:24', '2026-05-17 12:41:23', '2026-05-17 12:41:23', 1, 1, 0);
INSERT INTO `user_item_mastery` (`id`, `user_id`, `content_type`, `content_id`, `scope_type`, `scope_id`, `state`, `wrong_count`, `correct_streak`, `total_attempts`, `last_result`, `last_wrong_at`, `last_correct_at`, `last_practiced_at`, `next_review_at`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (3, 1, 'pinyin_pair', 116, 'book', 2, 'learning', 0, 1, 1, 1, NULL, '2026-05-17 04:41:24', '2026-05-17 04:41:24', '2026-05-17 04:41:24', '2026-05-17 12:41:23', '2026-05-17 12:41:23', 1, 1, 0);
INSERT INTO `user_item_mastery` (`id`, `user_id`, `content_type`, `content_id`, `scope_type`, `scope_id`, `state`, `wrong_count`, `correct_streak`, `total_attempts`, `last_result`, `last_wrong_at`, `last_correct_at`, `last_practiced_at`, `next_review_at`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (4, 1, 'pinyin_pair', 149, 'book', 2, 'learning', 0, 1, 1, 1, NULL, '2026-05-17 04:41:24', '2026-05-17 04:41:24', '2026-05-17 04:41:24', '2026-05-17 12:41:23', '2026-05-17 12:41:23', 1, 1, 0);
INSERT INTO `user_item_mastery` (`id`, `user_id`, `content_type`, `content_id`, `scope_type`, `scope_id`, `state`, `wrong_count`, `correct_streak`, `total_attempts`, `last_result`, `last_wrong_at`, `last_correct_at`, `last_practiced_at`, `next_review_at`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (5, 1, 'pinyin_pair', 65, 'book', 2, 'learning', 0, 1, 1, 1, NULL, '2026-05-17 04:41:24', '2026-05-17 04:41:24', '2026-05-17 04:41:24', '2026-05-17 12:41:23', '2026-05-17 12:41:23', 1, 1, 0);
INSERT INTO `user_item_mastery` (`id`, `user_id`, `content_type`, `content_id`, `scope_type`, `scope_id`, `state`, `wrong_count`, `correct_streak`, `total_attempts`, `last_result`, `last_wrong_at`, `last_correct_at`, `last_practiced_at`, `next_review_at`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (6, 1, 'pinyin_pair', 63, 'book', 2, 'learning', 0, 1, 1, 1, NULL, '2026-05-17 04:41:24', '2026-05-17 04:41:24', '2026-05-17 04:41:24', '2026-05-17 12:41:23', '2026-05-17 12:41:23', 1, 1, 0);
INSERT INTO `user_item_mastery` (`id`, `user_id`, `content_type`, `content_id`, `scope_type`, `scope_id`, `state`, `wrong_count`, `correct_streak`, `total_attempts`, `last_result`, `last_wrong_at`, `last_correct_at`, `last_practiced_at`, `next_review_at`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (7, 1, 'pinyin_pair', 115, 'book', 2, 'learning', 0, 1, 1, 1, NULL, '2026-05-17 04:41:24', '2026-05-17 04:41:24', '2026-05-17 04:41:24', '2026-05-17 12:41:23', '2026-05-17 12:41:23', 1, 1, 0);
INSERT INTO `user_item_mastery` (`id`, `user_id`, `content_type`, `content_id`, `scope_type`, `scope_id`, `state`, `wrong_count`, `correct_streak`, `total_attempts`, `last_result`, `last_wrong_at`, `last_correct_at`, `last_practiced_at`, `next_review_at`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (8, 1, 'pinyin_pair', 6, 'book', 2, 'learning', 0, 1, 1, 1, NULL, '2026-05-17 04:41:24', '2026-05-17 04:41:24', '2026-05-17 04:41:24', '2026-05-17 12:41:23', '2026-05-17 12:41:23', 1, 1, 0);
COMMIT;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `nickname` varchar(64) DEFAULT '',
  `role` enum('admin','student') NOT NULL DEFAULT 'student',
  `status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '1启用 0禁用',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` bigint(20) DEFAULT NULL,
  `updated_by` bigint(20) DEFAULT NULL,
  `is_deleted` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`,`is_deleted`),
  KEY `idx_role` (`role`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO `users` (`id`, `username`, `password_hash`, `nickname`, `role`, `status`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (1, 'admin', '$2b$12$ein8MZZHcWXndjxE0cPSxO7lpT6af7WJURBcW.4fb1gnYWnbzRUcW', '管理员', 'admin', 1, '2026-05-17 02:45:12', '2026-05-17 02:45:12', NULL, NULL, 0);
INSERT INTO `users` (`id`, `username`, `password_hash`, `nickname`, `role`, `status`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (2, 'test1', '$2b$12$wG0kB8pFnapaiDJaBd06VOCMTuG4pj.R40ziiAgB3Qrx3TCntHAt6', 't1', 'student', 1, '2026-05-17 12:45:12', '2026-05-17 12:45:12', 1, 1, 0);
INSERT INTO `users` (`id`, `username`, `password_hash`, `nickname`, `role`, `status`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (3, 't2', '$2b$12$hdRqlkPTBA9oELJMxtJa5uSC555sw70o7zCjQwJwPPH6GEC8SJbBa', 't2', 'student', 1, '2026-05-17 12:54:03', '2026-05-17 12:54:03', NULL, NULL, 0);
COMMIT;

-- ----------------------------
-- Table structure for word_libraries
-- ----------------------------
DROP TABLE IF EXISTS `word_libraries`;
CREATE TABLE `word_libraries` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `hanzi` varchar(16) NOT NULL,
  `pinyin` varchar(64) NOT NULL COMMENT '带声调',
  `pinyin_plain` varchar(64) NOT NULL COMMENT '无声调',
  `tone` tinyint(4) DEFAULT NULL,
  `remark` varchar(255) DEFAULT '',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` bigint(20) DEFAULT NULL,
  `updated_by` bigint(20) DEFAULT NULL,
  `is_deleted` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_hanzi` (`hanzi`,`is_deleted`)
) ENGINE=InnoDB AUTO_INCREMENT=176 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of word_libraries
-- ----------------------------
BEGIN;
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (1, '中', 'zhong1', 'zhong', NULL, '', '2026-05-17 02:51:53', '2026-05-17 02:51:53', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (2, '国', 'guo2', 'guo', NULL, '', '2026-05-17 02:51:58', '2026-05-17 02:51:58', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (3, '山', 'shan1', 'shan', NULL, '', '2026-05-17 02:52:04', '2026-05-17 02:52:04', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (4, '中国人', 'zhong1guo2ren2', 'zhongguoren', NULL, '', '2026-05-17 02:55:37', '2026-05-17 02:55:41', 1, 1, 1);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (5, '一', 'yi1', 'yi', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (6, '二', 'er4', 'er', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (7, '三', 'san1', 'san', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (8, '四', 'si4', 'si', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (9, '五', 'wu3', 'wu', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (10, '六', 'liu4', 'liu', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (11, '七', 'qi1', 'qi', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (12, '八', 'ba1', 'ba', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (13, '九', 'jiu3', 'jiu', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (14, '十', 'shi2', 'shi', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (15, '人', 'ren2', 'ren', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (16, '口', 'kou3', 'kou', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (17, '手', 'shou3', 'shou', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (18, '足', 'zu2', 'zu', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (19, '头', 'tou2', 'tou', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (20, '耳', 'er3', 'er', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (21, '目', 'mu4', 'mu', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (22, '鼻', 'bi2', 'bi', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (23, '舌', 'she2', 'she', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (24, '牙', 'ya2', 'ya', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (25, '水', 'shui3', 'shui', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (26, '火', 'huo3', 'huo', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (27, '土', 'tu3', 'tu', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (28, '金', 'jin1', 'jin', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (29, '木', 'mu4', 'mu', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (30, '日', 'ri4', 'ri', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (31, '月', 'yue4', 'yue', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (32, '星', 'xing1', 'xing', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (33, '云', 'yun2', 'yun', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (34, '雨', 'yu3', 'yu', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (35, '雪', 'xue3', 'xue', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (36, '风', 'feng1', 'feng', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (37, '雷', 'lei2', 'lei', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (38, '电', 'dian4', 'dian', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (39, '气', 'qi4', 'qi', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (40, '天', 'tian1', 'tian', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (41, '地', 'di4', 'di', NULL, '', '2026-05-17 02:58:02', '2026-05-17 02:58:02', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (42, '猫', 'mao1', 'mao', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (43, '狗', 'gou3', 'gou', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (44, '猪', 'zhu1', 'zhu', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (45, '牛', 'niu2', 'niu', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (46, '羊', 'yang2', 'yang', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (47, '马', 'ma3', 'ma', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (48, '鸡', 'ji1', 'ji', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (49, '鸭', 'ya1', 'ya', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (50, '鱼', 'yu2', 'yu', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (51, '鸟', 'niao3', 'niao', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (52, '花', 'hua1', 'hua', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (53, '草', 'cao3', 'cao', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (54, '树', 'shu4', 'shu', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (55, '叶', 'ye4', 'ye', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (56, '果', 'guo3', 'guo', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (57, '瓜', 'gua1', 'gua', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (58, '菜', 'cai4', 'cai', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (59, '豆', 'dou4', 'dou', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (60, '米', 'mi3', 'mi', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (61, '衣', 'yi1', 'yi', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (62, '食', 'shi2', 'shi', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (63, '住', 'zhu4', 'zhu', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (64, '行', 'xing2', 'xing', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (65, '床', 'chuang2', 'chuang', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (66, '桌', 'zhuo1', 'zhuo', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (67, '椅', 'yi3', 'yi', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (68, '灯', 'deng1', 'deng', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (69, '杯', 'bei1', 'bei', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (70, '碗', 'wan3', 'wan', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (71, '车', 'che1', 'che', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (72, '船', 'chuan2', 'chuan', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (73, '飞', 'fei1', 'fei', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (74, '机', 'ji1', 'ji', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (75, '自', 'zi4', 'zi', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (76, '摩', 'mo2', 'mo', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (77, '托', 'tuo1', 'tuo', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (78, '百', 'bai3', 'bai', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (79, '千', 'qian1', 'qian', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (80, '万', 'wan4', 'wan', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (81, '亿', 'yi4', 'yi', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (82, '零', 'ling2', 'ling', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (83, '个', 'ge4', 'ge', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (84, '只', 'zhi3', 'zhi', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (85, '条', 'tiao2', 'tiao', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (86, '把', 'ba3', 'ba', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (87, '本', 'ben3', 'ben', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (88, '张', 'zhang1', 'zhang', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (89, '匹', 'pi3', 'pi', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (90, '件', 'jian4', 'jian', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (91, '心', 'xin1', 'xin', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (92, '肝', 'gan1', 'gan', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (93, '脾', 'pi2', 'pi', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (94, '肺', 'fei4', 'fei', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (95, '肾', 'shen4', 'shen', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (96, '脚', 'jiao3', 'jiao', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (97, '指', 'zhi3', 'zhi', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (98, '掌', 'zhang3', 'zhang', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (99, '跑', 'pao3', 'pao', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (100, '跳', 'tiao4', 'tiao', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (101, '走', 'zou3', 'zou', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (102, '坐', 'zuo4', 'zuo', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (103, '立', 'li4', 'li', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (104, '卧', 'wo4', 'wo', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (105, '吃', 'chi1', 'chi', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (106, '喝', 'he1', 'he', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (107, '看', 'kan4', 'kan', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (108, '听', 'ting1', 'ting', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (109, '大', 'da4', 'da', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (110, '小', 'xiao3', 'xiao', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (111, '多', 'duo1', 'duo', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (112, '少', 'shao3', 'shao', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (113, '高', 'gao1', 'gao', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (114, '矮', 'ai3', 'ai', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (115, '胖', 'pang4', 'pang', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (116, '瘦', 'shou4', 'shou', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (117, '美', 'mei3', 'mei', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (118, '丑', 'chou3', 'chou', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (119, '快', 'kuai4', 'kuai', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (120, '慢', 'man4', 'man', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (121, '好', 'hao3', 'hao', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (122, '坏', 'huai4', 'huai', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (123, '早', 'zao3', 'zao', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (124, '晚', 'wan3', 'wan', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (125, '远', 'yuan3', 'yuan', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (126, '近', 'jin4', 'jin', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (127, '真', 'zhen1', 'zhen', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (128, '假', 'jia3', 'jia', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (129, '工', 'gong1', 'gong', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (130, '厂', 'chang3', 'chang', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (131, '作', 'zuo4', 'zuo', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (132, '长', 'zhang3', 'zhang', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (133, '房', 'fang2', 'fang', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (134, '家', 'jia1', 'jia', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (135, '上', 'shang4', 'shang', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (136, '学', 'xue2', 'xue', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (137, '升', 'sheng1', 'sheng', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (138, '面', 'mian4', 'mian', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (139, '下', 'xia4', 'xia', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (140, '降', 'jiang4', 'jiang', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (141, '左', 'zuo3', 'zuo', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (142, '边', 'bian1', 'bian', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (143, '转', 'zhuan3', 'zhuan', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (144, '右', 'you4', 'you', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (145, '前', 'qian2', 'qian', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (146, '进', 'jin4', 'jin', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (147, '后', 'hou4', 'hou', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (148, '退', 'tui4', 'tui', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (149, '里', 'li3', 'li', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (150, '程', 'cheng2', 'cheng', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (151, '外', 'wai4', 'wai', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (152, '出', 'chu1', 'chu', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (153, '东', 'dong1', 'dong', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (154, '方', 'fang1', 'fang', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (155, '南', 'nan2', 'nan', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (156, '西', 'xi1', 'xi', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (157, '北', 'bei3', 'bei', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (158, '京', 'jing1', 'jing', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (159, '庭', 'ting2', 'ting', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (160, '回', 'hui2', 'hui', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (161, '习', 'xi2', 'xi', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (162, '校', 'xiao4', 'xiao', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (163, '生', 'sheng1', 'sheng', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (164, '园', 'yuan2', 'yuan', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (165, '爱', 'ai4', 'ai', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (166, '情', 'qing2', 'qing', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (167, '事', 'shi4', 'shi', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (168, '朋', 'peng2', 'peng', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (169, '友', 'you3', 'you', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (170, '亲', 'qin1', 'qin', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (171, '辈', 'bei4', 'bei', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (172, '谊', 'yi4', 'yi', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (173, '认', 'ren4', 'ren', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (174, '识', 'shi2', 'shi', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
INSERT INTO `word_libraries` (`id`, `hanzi`, `pinyin`, `pinyin_plain`, `tone`, `remark`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`) VALUES (175, '为', 'wei4', 'wei', NULL, '练习册批量导入', '2026-05-17 12:16:18', '2026-05-17 12:16:18', 1, 1, 0);
COMMIT;

-- ----------------------------
-- Table structure for wrong_questions
-- ----------------------------
DROP TABLE IF EXISTS `wrong_questions`;
CREATE TABLE `wrong_questions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `book_id` bigint(20) NOT NULL,
  `hanzi` varchar(16) NOT NULL,
  `pinyin` varchar(64) NOT NULL,
  `wrong_count` int(11) NOT NULL DEFAULT '1',
  `last_wrong_at` datetime NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` bigint(20) DEFAULT NULL,
  `updated_by` bigint(20) DEFAULT NULL,
  `is_deleted` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_hanzi` (`user_id`,`hanzi`,`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of wrong_questions
-- ----------------------------
BEGIN;
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
