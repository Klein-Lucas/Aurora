from aurora.schemas import TaskResponse, TaskCreate, TaskUpdate
from aurora.storage.sqlite_storage import SQLiteStorage
from aurora.crud import TaskCRUD
from aurora.task import Task
from uuid import UUID
from fastapi import APIRouter, Depends

def get_crud() -> TaskCRUD:
    storage = SQLiteStorage()
    return TaskCRUD(storage=storage)

router = APIRouter(prefix="/tasks")

@router.post("", status_code=201)
def create_task(task: TaskCreate, crud: TaskCRUD = Depends(get_crud)) -> TaskResponse:
    task = Task(**task.model_dump())
    return crud.create_task(task=task)

@router.get("", status_code=200)
def get_tasks(crud: TaskCRUD = Depends(get_crud)) -> list[TaskResponse]:
    return crud.read_all()

@router.get("/{id}", status_code=200)
def get_task(id: UUID, crud: TaskCRUD = Depends(get_crud)) -> TaskResponse:
    return crud.read_by_id(id=id)

@router.patch("/{id}", status_code=200)
def update_task(id: UUID, updated_fields: TaskUpdate, crud: TaskCRUD = Depends(get_crud)) -> TaskResponse:
    updated_fields = updated_fields.model_dump(exclude_unset=True)
    task = crud.read_by_id(id=id)
    task = task.model_dump()
    task.update(updated_fields)
    return crud.update_task(Task.model_validate(task))

@router.delete("/{id}", status_code=200)
def delete_task(id: UUID, crud: TaskCRUD = Depends(get_crud)) -> TaskResponse:
    return crud.delete_by_id(id=id)