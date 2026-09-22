from pathlib import Path
import pytest
from uuid import uuid4
from aurora.crud import TaskCRUD
from aurora.storage.json_storage import JSONStorage
from aurora.storage.sqlite_storage import SQLiteStorage
from aurora.task import Task
from aurora.exceptions import TaskNotFoundError

@pytest.fixture(params=["json", "sqlite"])
def crud(request, tmp_path: Path):
    if request.param == "json":
        storage = JSONStorage(path=tmp_path / "test.json")
    else:
        storage = SQLiteStorage(path=tmp_path / "test.db")
    return TaskCRUD(storage=storage)

@pytest.fixture
def crud_with_tasks(crud: TaskCRUD):
    crud.create_task(Task(title="Test Task 1"))
    crud.create_task(Task(title="Test Task 2"))
    return crud

@pytest.fixture
def sample_task():
    return Task(title="Sample task")

def test_create_task(crud: TaskCRUD, sample_task: Task):
    crud.create_task(task=sample_task)
    assert len(crud.read_all()) == 1

def test_read_all(crud_with_tasks: TaskCRUD):
    assert len(crud_with_tasks.read_all()) == 2

def test_read_by_id_found(crud: TaskCRUD, sample_task: Task):
    crud.create_task(task=sample_task) # Creates a new task to use its ID
    found = crud.read_by_id(sample_task.id)
    assert sample_task.id == found.id

def test_read_by_id_not_found(crud: TaskCRUD):
    uuid_inexistent = uuid4()
    with pytest.raises(TaskNotFoundError):
        crud.read_by_id(id=uuid_inexistent)

def test_update_task(crud: TaskCRUD, sample_task: Task):
    crud.create_task(task=sample_task)
    sample_task.title = "Updated title"
    updated = crud.update_task(updated_task=sample_task)
    assert updated.title == "Updated title"
    assert crud.read_by_id(id=sample_task.id).title == "Updated title"

def test_update_task_not_found(crud: TaskCRUD, sample_task: Task):
    with pytest.raises(TaskNotFoundError):
        crud.update_task(updated_task=sample_task)

def test_delete_task(crud: TaskCRUD, sample_task: Task):
    crud.create_task(task=sample_task)
    deleted = crud.delete_by_id(id=sample_task.id)
    assert deleted.id == sample_task.id
    assert crud.read_all() == []

def test_delete_task_not_found(crud: TaskCRUD):
    uuid_inexistent = uuid4()
    with pytest.raises(TaskNotFoundError):
        crud.delete_by_id(id=uuid_inexistent)