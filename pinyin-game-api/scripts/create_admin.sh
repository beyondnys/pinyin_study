#!/usr/bin/env bash
# 在 pinyin-game-api 目录下创建默认管理员 admin / admin123
set -e
cd "$(dirname "$0")/.."
if [ -f venv/bin/activate ]; then
  # shellcheck source=/dev/null
  source venv/bin/activate
elif [ -f .venv/bin/activate ]; then
  # shellcheck source=/dev/null
  source .venv/bin/activate
fi
python -m app.scripts.init_admin "$@"
