from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from aurora.routes.tasks import router
from aurora.exceptions import TaskNotFoundError

app = FastAPI()

app.include_router(router=router)


@app.exception_handler(TaskNotFoundError)
def task_not_found_handler(request: Request, exc: TaskNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})