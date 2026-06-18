from aurora.task import TaskBase, Task

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: str | None = None

class TaskResponse(Task):
    pass