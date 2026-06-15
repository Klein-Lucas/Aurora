from aurora.storage import StorageProtocol
from aurora.task import Task
from uuid import UUID

class TaskCRUD():
    def __init__(self, storage: StorageProtocol):
        self.storage = storage
    
    # Create
    def create_task(self, task: Task):
        self.storage.create_task(task=task)

    # Read    
    def read_by_id(self, id: UUID) -> Task:
        return self.storage.get_task(id=id)

    
    def read_all(self) -> list[Task]:
        return self.storage.get_all()

    # Update
    def update_task(self, updated_task: Task):
        self.storage.update(updated_task=updated_task)

    # Delete
    def delete_by_id(self, id: UUID):
        self.storage.delete(id=id)