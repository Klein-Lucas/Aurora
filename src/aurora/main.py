from fastapi import FastAPI
from aurora.routes.tasks import router

app = FastAPI()

app.include_router(router=router)