-- 演示练习册与题目（需先执行 init.sql）
-- 执行: mysql -u pinyin_game -p pinyin_game < sql/seed_demo.sql

USE pinyin_game;

INSERT INTO practice_books (title, description, question_count, status, is_deleted)
SELECT '拼音练习册（一年级）', '山山水田风云花雨禾石对，每次随机 8 题配对', 10, 1, 0
FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM practice_books WHERE title = '拼音练习册（一年级）' AND is_deleted = 0
);

SET @book_id = (SELECT id FROM practice_books WHERE title = '拼音练习册（一年级）' AND is_deleted = 0 LIMIT 1);

-- 题目拼音请用 Python 脚本生成（与 pypinyin 一致）：
--   cd pinyin-game-api && python -m app.scripts.seed_demo_data
