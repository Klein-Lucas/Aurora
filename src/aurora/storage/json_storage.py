from aurora.task import Task, Category, Status
from uuid import UUID
from aurora.exceptions import TaskNotFoundError
import json
from aurora.config import DATA_DIR
from pathlib import Path
from datetime import date
from enum import Enum
from dataclasses import asdict

class JSONStorage:
    _JSON_FILE = DATA_DIR / "db.json"

    def __init__(self, path: Path = _JSON_FILE):
        self.path = path
    
    @staticmethod
    def _find_in_list(data: list[Task], id: UUID) -> int:
        for i,task in enumerate(data):
            if task.id == id:
                return i
        # If the task is not found
        raise TaskNotFoundError(f"Task com id '{id}' não encontrada")

    @staticmethod
    def _serialize(obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.value
        raise TypeError(f"Tipo não serializável: {type(obj)}")

    def _deserialize(self, data: dict) -> Task:
        return Task(
            id = UUID(data["id"]),
            title = data["title"],
            status = Status(data["status"]),
            created_at = date.fromisoformat(data["created_at"]),
            sub_tasks = [self._deserialize(task) for task in data.get("sub_tasks",[])],
            description = data.get("description"),
            end_date = date.fromisoformat(data.get("end_date")) if data.get("end_date") else None,
            start_date = date.fromisoformat(data.get("start_date")) if data.get("start_date") else None,
            category = Category(data.get("category")) if data.get("category") else None,
        )

    def _save(self, tasks: list[Task]):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        data = [asdict(task) for task in tasks]
        with open(self.path, "w") as file:
            json.dump(data, file, default=self._serialize, indent=2)

    def _load(self) -> list[Task]:
        try:
            with open(self.path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            return []
        return [self._deserialize(task) for task in data]
    
    def create(self, task : Task) -> None:
        data = self._load()
        data.append(task)
        self._save(data)

    def get_task(self, id : UUID) -> Task:
        data = self._load()
        task_index = self._find_in_list(data, id)
        return data[task_index]

    def get_all(self) -> list[Task]:
        return self._load()

    def update(self, updated_task : Task) -> None:
        data = self._load()
        task_index = self._find_in_list(data=data, id=updated_task.id)
        data[task_index] = updated_task
        self._save(data)


    def delete(self, id : UUID) -> None:
        data = self._load()
        task_index = self._find_in_list(data=data, id=id)
        data.pop(task_index)
        self._save(data)