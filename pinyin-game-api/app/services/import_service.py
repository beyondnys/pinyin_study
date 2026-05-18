"""文本导入服务：从课文生成练习册与题目。"""

from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from app.models.import_task import ImportTask
from app.models.practice_book import PracticeBook
from app.models.practice_question import PracticeQuestion
from app.models.word_library import WordLibrary
from app.services.pinyin_service import extract_unique_hanzi, hanzi_to_pinyin
from app.utils.pinyin_util import apply_pinyin_fields
from app.utils.datetime_util import utc_now


def process_import_task(
    db: Session,
    task: ImportTask,
    book_title: Optional[str],
    operator_id: int,
) -> ImportTask:
    """
    同步处理导入任务（MVP 同步执行）。
    解析汉字、生成拼音、写入字库与练习册题目。
    """
    task.status = "processing"
    db.commit()

    try:
        hanzi_list = extract_unique_hanzi(task.raw_text)
        if not hanzi_list:
            task.status = "failed"
            task.result_message = "未识别到汉字"
            db.commit()
            return task

        title = book_title or task.title
        book = PracticeBook(
            title=title,
            description=f"由导入任务「{task.title}」自动生成",
            question_count=0,
            status=1,
            created_by=operator_id,
            updated_by=operator_id,
        )
        db.add(book)
        db.flush()

        sort_order = 0
        for hz in hanzi_list:
            py_result = hanzi_to_pinyin(hz)

            # 字库 upsert
            word = (
                db.query(WordLibrary)
                .filter(WordLibrary.hanzi == hz, WordLibrary.is_deleted == 0)
                .first()
            )
            if not word:
                word = WordLibrary(
                    hanzi=hz,
                    pinyin="",
                    pinyin_list="[]",
                    pinyin_plain="",
                    created_by=operator_id,
                    updated_by=operator_id,
                )
                apply_pinyin_fields(word, py_result)
                db.add(word)
            elif not word.pinyin:
                apply_pinyin_fields(word, py_result)

            q = PracticeQuestion(
                book_id=book.id,
                hanzi=hz,
                pinyin="",
                pinyin_list="[]",
                sort_order=sort_order,
                created_by=operator_id,
                updated_by=operator_id,
            )
            apply_pinyin_fields(q, py_result)
            db.add(q)
            sort_order += 1

        book.question_count = sort_order
        task.book_id = book.id
        task.status = "done"
        task.result_message = f"成功导入 {sort_order} 个汉字"
        db.commit()
        return task
    except Exception as e:
        db.rollback()
        task = db.query(ImportTask).filter(ImportTask.id == task.id).first()
        task.status = "failed"
        task.result_message = str(e)[:500]
        db.commit()
        return task
