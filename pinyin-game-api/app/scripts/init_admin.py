"""
初始化管理员账号。

默认账号：admin / admin123

用法（在 pinyin-game-api 目录下）：
    python -m app.scripts.init_admin
    python -m app.scripts.init_admin --username admin --password your_pass
    python -m app.scripts.init_admin --reset   # 已存在时重置密码
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# 将项目根目录加入 path，支持直接 python app/scripts/init_admin.py
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.database import SessionLocal
from app.models.user import User
from app.utils.password_util import hash_password

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin123"


def create_or_reset_admin(
    username: str = DEFAULT_USERNAME,
    password: str = DEFAULT_PASSWORD,
    nickname: str = "管理员",
    reset: bool = False,
) -> None:
    """
    创建或重置管理员用户。

    :param username: 登录名
    :param password: 明文密码（入库前 bcrypt 哈希）
    :param nickname: 显示昵称
    :param reset: True 时若用户已存在则更新密码与角色
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username, User.is_deleted == 0).first()
        if user:
            if not reset:
                print(f"用户「{username}」已存在。若要重置密码请加参数 --reset")
                return
            user.password_hash = hash_password(password)
            user.role = "admin"
            user.status = 1
            user.nickname = nickname or user.nickname
            db.commit()
            print(f"已重置管理员密码：用户名 {username}")
            return

        user = User(
            username=username,
            password_hash=hash_password(password),
            nickname=nickname,
            role="admin",
            status=1,
        )
        db.add(user)
        db.commit()
        print(f"已创建管理员：用户名 {username}，密码 {password}")
        print("请登录后立即修改默认密码。")
    except Exception as e:
        db.rollback()
        print(f"失败: {e}")
        raise
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="创建或重置拼音练习系统管理员")
    parser.add_argument("--username", "-u", default=DEFAULT_USERNAME, help="管理员用户名")
    parser.add_argument("--password", "-p", default=DEFAULT_PASSWORD, help="管理员密码")
    parser.add_argument("--nickname", "-n", default="管理员", help="昵称")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="用户已存在时重置为 admin 角色并更新密码",
    )
    args = parser.parse_args()
    create_or_reset_admin(
        username=args.username,
        password=args.password,
        nickname=args.nickname,
        reset=args.reset,
    )


if __name__ == "__main__":
    main()
