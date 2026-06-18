from aurora.schemas import TaskResponse
from aurora.storage.sqlite_storage import SQLiteStorage
from aurora.crud import TaskCRUD
from fastapi import APIRouter, Depends

def get_crud() -> TaskCRUD:
    storage = SQLiteStorage()
    return TaskCRUD(storage=storage)

router = APIRouter(prefix="/tasks")

@router.get("")
def get_tasks(crud: TaskCRUD = Depends(get_crud)) -> list[TaskResponse]:
    return crud.read_all()