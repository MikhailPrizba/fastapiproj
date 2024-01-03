from sqlalchemy import delete, desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from typing import Union
from tasks.schemas import TaskSchema, TaskSchemaAdd
from tasks.models import Tasks


class TaskRepository:
    model = Tasks  # type: ignore
    create_scheme = TaskSchemaAdd  # type: ignore

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, author_id: id, input_data: create_scheme) -> model:
        task = self.model(author_id=author_id, **input_data.model_dump())
        self._session.add(task)
        await self._session.commit()
        await self._session.refresh(task)
        return task

    async def retrieve(self, pk: id) -> Tasks:
        res = await self._session.execute(select(self.model).where(self.model.id == pk))
        task = res.scalars().first()
        self.check_object(task)
        await self._session.refresh(task)
        return task

    async def get_user_task(self, author_id: id) -> Tasks:
        res = await self._session.execute(
            select(self.model).where(self.model.author_id == author_id)
        )
        tasks = res.scalars().all()
        return tasks
