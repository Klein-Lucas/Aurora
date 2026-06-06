from pathlib import Path

import pytest
from uuid import uuid4
from aurora.crud import TaskCRUD
from aurora.storage import JSONStorage
from aurora.task import Task
from aurora.exceptions import TaskNotFoundError

@pytest.fixture
def crud(tmp_path: Path):
    temp_dir = JSONStorage(path=tmp_path / "test.json")
    return TaskCRUD(storage=temp_dir)

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