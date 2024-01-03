from fastapi import FastAPI

from auth.router import router as auth_router
from tasks.router import router as tasks_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(tasks_router)
