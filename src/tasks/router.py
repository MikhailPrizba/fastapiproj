from typing import Annotated

from fastapi import APIRouter, Depends

from .services.services import provide_task_service
from tasks.schemas import TaskSchemaAdd
from sqlalchemy.ext.asyncio import AsyncSession
from auth.dependencies.auth import get_current_user
from base import get_async_session

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post("")
async def add_task(
    task: TaskSchemaAdd,
    author_id: id = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    service = provide_task_service(session)
    task = await service.add(int(author_id), task)
    return task


@router.get("/")
async def get_tasks(
    author_id: id = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    service = provide_task_service(session)
    tasks = await service.get_user_task(author_id=int(author_id))
    return tasks
