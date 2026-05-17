"""
自适应掌握度模块（与错题本 wrong_questions 独立）。

- 粒度：用户 + 内容项 + 场景(scope)
- 加权抽题、streak、复习间隔
- 可扩展词语/成语等 ContentType + Provider
"""

from app.learning.service import LearningMasteryService, book_scope

__all__ = ["LearningMasteryService", "book_scope"]
