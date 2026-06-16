from aurora.config import DATA_DIR
from aurora.task import Task, Category, Status
from aurora.exceptions import TaskNotFoundError
from pathlib import Path
import sqlite3
from contextlib import contextmanager
from datetime import date
from uuid import UUID

class SQLiteStorage:
    _DB_FILE = DATA_DIR / "sqlite_db.db"

    def __init__(self, path: Path = _DB_FILE):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._get_connection() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks(
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    start_date TEXT,
                    end_date TEXT,
                    description TEXT,
                    category TEXT,
                    status TEXT NOT NULL,
                    created_at TEXT,
                    parent_id TEXT,
                    FOREIGN KEY (parent_id) REFERENCES tasks(id))
                """)

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.path)
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn.cursor()
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    @staticmethod
    def _task_to_row(task: Task) -> tuple:
        return(
            str(task.id),
            task.title,
            date.isoformat(task.start_date) if task.start_date else None,
            date.isoformat(task.end_date) if task.end_date else None,
            task.description,
            task.category.value if task.category else None,
            task.status.value if task.status else None,
            date.isoformat(task.created_at) if task.created_at else None,
            str(task.parent_id) if task.parent_id else None
        )
    
    @staticmethod
    def _row_to_task(task: tuple) -> Task:
        return Task(
            id=UUID(task[0]),
            title=task[1],
            start_date=date.fromisoformat(task[2]) if task[2] else None,
            end_date=date.fromisoformat(task[3]) if task[3] else None,
            description=task[4],
            category=Category(task[5]) if task[5] else None,
            status=Status(task[6]) if task[6] else None,
            created_at=date.fromisoformat(task[7]) if task[7] else None,
            parent_id=UUID(task[8]) if task[8] else None
        )
    
    @staticmethod
    def _find_by_id(cur: sqlite3.Cursor, id: UUID) -> tuple:
        cur.execute("SELECT * FROM tasks WHERE id = ?",(str(id),))
        result = cur.fetchone()
        if result is not None:
            return result
        raise TaskNotFoundError(id)
        
    
    def create_task(self, task: Task):
        query_params = self._task_to_row(task=task)
        with self._get_connection() as cur:
            cur.execute("INSERT INTO tasks VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", query_params)
        

    def get_task(self, id: UUID) -> Task:
        with self._get_connection() as cur:
            result = self._find_by_id(cur=cur, id=id)
        return self._row_to_task(result)
        

    def get_all(self) -> list[Task]:
        with self._get_connection() as cur:
            cur.execute("SELECT * FROM tasks")
            result = cur.fetchall()
            tasks = [self._row_to_task(task) for task in result]
            return tasks

    def update(self, updated_task: Task):
        t = self._task_to_row(updated_task)
        with self._get_connection() as cur:
            self._find_by_id(cur=cur, id=updated_task.id)
            cur.execute("""UPDATE OR FAIL tasks SET 
                        title=?,
                        start_date=?,
                        end_date=?,
                        description=?,
                        category=?,
                        status=?,
                        created_at=?,
                        parent_id=?
                        WHERE id=?""", 
                        (t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[0]))

    def delete(self, id: UUID):
        with self._get_connection() as cur:
            self._find_by_id(cur=cur, id=id)
            cur.execute("DELETE FROM tasks WHERE id=?", (str(id),))