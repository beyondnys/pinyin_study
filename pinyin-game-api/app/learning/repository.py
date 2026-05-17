"""掌握度持久化。"""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional

from sqlalchemy.orm import Session

from app.learning.mastery_engine import default_row, row_from_orm
from app.learning.types import ContentRef, ContentType, LearningScope, MasteryRowData, ScopeType
from app.models.user_item_mastery import UserItemMastery
from app.utils.datetime_util import utc_now


def _scope_fields(scope: LearningScope) -> tuple[str, int]:
    return scope.scope_type.value, scope.scope_id


class MasteryRepository:
    """user_item_mastery 读写。"""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_map(
        self,
        user_id: int,
        scope: LearningScope,
        content_type: ContentType,
        content_ids: Iterable[int],
    ) -> Dict[int, MasteryRowData]:
        """批量读取 content_id -> 掌握度。"""
        ids = list(content_ids)
        if not ids:
            return {}
        st, sid = _scope_fields(scope)
        rows = (
            self.db.query(UserItemMastery)
            .filter(
                UserItemMastery.user_id == user_id,
                UserItemMastery.content_type == content_type.value,
                UserItemMastery.scope_type == st,
                UserItemMastery.scope_id == sid,
                UserItemMastery.content_id.in_(ids),
                UserItemMastery.is_deleted == 0,
            )
            .all()
        )
        return {r.content_id: row_from_orm(r) for r in rows}

    def get_or_create_row(
        self,
        user_id: int,
        scope: LearningScope,
        content: ContentRef,
        operator_id: int,
    ) -> UserItemMastery:
        """获取或创建掌握度行。"""
        st, sid = _scope_fields(scope)
        row = (
            self.db.query(UserItemMastery)
            .filter(
                UserItemMastery.user_id == user_id,
                UserItemMastery.content_type == content.content_type.value,
                UserItemMastery.content_id == content.content_id,
                UserItemMastery.scope_type == st,
                UserItemMastery.scope_id == sid,
                UserItemMastery.is_deleted == 0,
            )
            .first()
        )
        if row:
            return row

        now = utc_now()
        row = UserItemMastery(
            user_id=user_id,
            content_type=content.content_type.value,
            content_id=content.content_id,
            scope_type=st,
            scope_id=sid,
            state="unseen",
            wrong_count=0,
            correct_streak=0,
            total_attempts=0,
            last_result=None,
            created_by=operator_id,
            updated_by=operator_id,
            last_practiced_at=None,
            next_review_at=None,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def save_row_data(
        self,
        orm_row: UserItemMastery,
        data: MasteryRowData,
        operator_id: int,
    ) -> None:
        """将内存状态写回 ORM。"""
        orm_row.state = data.state.value
        orm_row.wrong_count = data.wrong_count
        orm_row.correct_streak = data.correct_streak
        orm_row.last_result = data.last_result
        orm_row.last_wrong_at = data.last_wrong_at
        orm_row.last_correct_at = data.last_correct_at
        orm_row.last_practiced_at = data.last_practiced_at
        orm_row.next_review_at = data.next_review_at
        orm_row.updated_by = operator_id
