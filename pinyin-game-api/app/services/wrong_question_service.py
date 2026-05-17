"""错题本服务。"""

from __future__ import annotations
from sqlalchemy.orm import Session

from app.models.wrong_question import WrongQuestion
from app.utils.datetime_util import utc_now


def upsert_wrong_questions(
    db: Session,
    user_id: int,
    items: list[tuple[str, str, int]],
) -> None:
    """
    批量更新错题本。
    items: [(hanzi, pinyin, book_id), ...]
    """
    now = utc_now()
    for hanzi, pinyin, book_id in items:
        row = (
            db.query(WrongQuestion)
            .filter(
                WrongQuestion.user_id == user_id,
                WrongQuestion.hanzi == hanzi,
                WrongQuestion.is_deleted == 0,
            )
            .first()
        )
        if row:
            row.wrong_count += 1
            row.pinyin = pinyin
            row.book_id = book_id
            row.last_wrong_at = now
            row.updated_by = user_id
        else:
            db.add(
                WrongQuestion(
                    user_id=user_id,
                    book_id=book_id,
                    hanzi=hanzi,
                    pinyin=pinyin,
                    wrong_count=1,
                    last_wrong_at=now,
                    created_by=user_id,
                    updated_by=user_id,
                )
            )
