from .task import Task, Category, Status
import json
from pathlib import Path
import uuid
from datetime import date
from enum import Enum
from dataclasses import asdict

DATA_DIR = Path(__file__).parent.parent.parent / "data"
DB_FILE = DATA_DIR / "db.json"

def serialize(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, Enum):
        return obj.value
    raise TypeError(f"Tipo não serializável: {type(obj)}")

def deserialize(data: dict) -> Task:
    return Task(
        id = uuid.UUID(data["id"]),
        title = data["title"],
        status = Status(data["status"]),
        created_at = date.fromisoformat(data["created_at"]),
        sub_tasks = [deserialize(task) for task in data.get("sub_tasks",[])],
        description = data.get("description"),
        end_date = date.fromisoformat(data.get("end_date")) if data.get("end_date") else None,
        start_date = date.fromisoformat(data.get("start_date")) if data.get("start_date") else None,
        category = Category(data.get("category")) if data.get("category") else None,
    )

class JSONStorage:
    def __init__(self, path: Path = DB_FILE):
        self.path = path

    def save(self, tasks: list[Task]):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        data = [asdict(task) for task in tasks]
        with open(self.path, "w") as file:
            json.dump(data, file, default=serialize, indent=2)

    def load(self) -> list[Task]:
        try:
            with open(self.path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            return []
        return [deserialize(task) for task in data]