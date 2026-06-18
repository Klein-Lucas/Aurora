from aurora.task import TaskBase, Task
from aurora.exceptions import MissingRequiredFieldError
from pydantic import field_validator

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: str | None = None

class TaskResponse(Task):
    pass