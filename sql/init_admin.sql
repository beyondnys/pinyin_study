-- 创建默认管理员：admin / admin123
-- 密码为 bcrypt 哈希（与后端 passlib/bcrypt 兼容）
-- 使用前请先执行 init.sql 建库建表

USE pinyin_game;

-- 若已存在则先删除（可按需注释掉）
DELETE FROM users WHERE username = 'admin' AND is_deleted = 0;

INSERT INTO users (
  username,
  password_hash,
  nickname,
  role,
  status,
  is_deleted
) VALUES (
  'admin',
  '$2b$12$ein8MZZHcWXndjxE0cPSxO7lpT6af7WJURBcW.4fb1gnYWnbzRUcW',
  '管理员',
  'admin',
  1,
  0
);
