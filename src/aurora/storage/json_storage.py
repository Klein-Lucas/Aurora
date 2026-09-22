from aurora.task import Task
from uuid import UUID
from aurora.exceptions import TaskNotFoundError
import json
from aurora.config import DATA_DIR
from pathlib import Path


class JSONStorage:
    _JSON_FILE = DATA_DIR / "json_db.json"

    def __init__(self, path: Path = _JSON_FILE):
        self.path = path
    
    @staticmethod
    def _find_in_list(data: list[Task], id: UUID) -> int:
        for i,task in enumerate(data):
            if task.id == id:
                return i
        # If the task is not found
        raise TaskNotFoundError(id)

    def _save(self, tasks: list[Task]):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = [task.model_dump(mode="json") for task in tasks]
        with open(self.path, "w") as file:
            json.dump(data, file, indent=2)

    def _load(self) -> list[Task]:
        try:
            with open(self.path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            return []
        return [Task.model_validate(task) for task in data]
    
    def create_task(self, task: Task) -> Task:
        data = self._load()
        data.append(task)
        self._save(data)
        return task

    def get_task(self, id: UUID) -> Task:
        data = self._load()
        task_index = self._find_in_list(data, id)
        return data[task_index]

    def get_all(self) -> list[Task]:
        return self._load()

    def update(self, updated_task: Task) -> Task:
        data = self._load()
        task_index = self._find_in_list(data=data, id=updated_task.id)
        data[task_index] = updated_task
        self._save(data)
        return updated_task


    def delete(self, id: UUID) -> Task:
        data = self._load()
        task_index = self._find_in_list(data=data, id=id)
        removed_task = data.pop(task_index)
        self._save(data)
        return removed_task