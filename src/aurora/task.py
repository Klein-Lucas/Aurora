from dataclasses import dataclass, field
from datetime import date
import uuid
from enum import Enum
from .exceptions import MissingRequiredFieldError

class Status(Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    DELETED = "deleted"

class Category(Enum):
    WORK = "work"
    STUDY = "study"
    HEALTH = "health"
    HOBBY = "hobby"

@dataclass
class Task:
    # Required
    title: str
    # Optional
    start_date: date | None = None
    end_date: date | None = None
    description: str | None = None
    category: Category | None = None
    sub_tasks: "list[Task]" = field(default_factory=list)
    # Default
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: date = field(default_factory=date.today)
    status: Status = field(default=Status.NEW)

    def __post_init__(self):
        if not self.title:
            raise MissingRequiredFieldError(["title"])