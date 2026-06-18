from pydantic import BaseModel, Field, field_validator
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

class TaskBase(BaseModel):
    # Required
    title: str
    # Optional
    start_date: date | None = None
    end_date: date | None = None
    description: str | None = None
    category: Category | None = None
    parent_id: uuid.UUID | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise MissingRequiredFieldError(["title"])
        return value

class Task(TaskBase):
    # Default
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_at: date = Field(default_factory=date.today)
    status: Status = Field(default=Status.NEW)