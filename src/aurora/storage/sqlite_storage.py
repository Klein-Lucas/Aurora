from aurora.config import DATA_DIR
from aurora.task import Task
from aurora.exceptions import TaskNotFoundError
from pathlib import Path
import sqlite3
from contextlib import contextmanager
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
        conn.row_factory = sqlite3.Row
        try:
            yield conn.cursor()
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    @staticmethod
    def _task_to_row(task: Task) -> dict:
        return task.model_dump(mode="json")
    
    @staticmethod
    def _row_to_task(task: sqlite3.Row) -> Task:
        task = dict(task)
        return Task.model_validate(task)
    
    @staticmethod
    def _insert_clause() -> str:
        fields = Task.model_fields.keys()
        columns = ", ".join(fields)
        placeholders = ", ".join(f":{field}" for field in fields)
        return f"({columns}) VALUES ({placeholders})"

    @staticmethod
    def _update_clause() -> str:
        fields = Task.model_fields.keys() - {"id"} # Remove ID from updated columns
        placeholders = ", ".join(f"{field}= :{field}" for field in fields)
        return placeholders
        
    
    @staticmethod
    def _find_by_id(cur: sqlite3.Cursor, id: UUID) -> tuple:
        cur.execute("SELECT * FROM tasks WHERE id = ?",(str(id),))
        result = cur.fetchone()
        if result is not None:
            return result
        raise TaskNotFoundError(id)
        
    
    def create_task(self, task: Task):
        query_params = self._task_to_row(task=task)
        query = "INSERT INTO tasks " + self._insert_clause()
        with self._get_connection() as cur:
            cur.execute(query, query_params)
        

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
        query_params = self._task_to_row(updated_task)
        query = "UPDATE OR FAIL tasks SET " + self._update_clause() + " WHERE id = :id"
        with self._get_connection() as cur:
            self._find_by_id(cur=cur, id=updated_task.id)
            cur.execute(query, query_params)

    def delete(self, id: UUID):
        with self._get_connection() as cur:
            self._find_by_id(cur=cur, id=id)
            cur.execute("DELETE FROM tasks WHERE id=?", (str(id),))