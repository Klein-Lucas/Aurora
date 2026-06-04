from .storage import JSONStorage
from .task import Task
from uuid import UUID
from .exceptions import TaskNotFoundError

class TaskCRUD():
    def __init__(self, storage: JSONStorage):
        self.storage = storage

    # Create
    def create_task(self, task: Task):
        data = self.storage.load()
        data.append(task)
        self.storage.save(data)

    # Read
    @staticmethod
    def _find_in_list(data: list[Task], id: UUID) -> Task:
        for task in data:
            if task.id == id:
                return task
        raise TaskNotFoundError(id)
    
    def read_by_id(self, id: UUID) -> Task:
        data = self.storage.load()
        return self._find_in_list(data, id)
    
    def read_all(self) -> list[Task]:
        return self.storage.load()

    # Update
    def update_task(self, updated_task: Task):
        data = self.storage.load()
        existent_task = self._find_in_list(data, updated_task.id)
        data.remove(existent_task)
        data.append(updated_task)
        self.storage.save(data)

    # Delete
    def delete_by_id(self, id: UUID):
        data = self.storage.load()
        selected_task = self._find_in_list(data, id)
        data.remove(selected_task)
        self.storage.save(data)