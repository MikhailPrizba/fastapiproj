from tasks.repositories.task import TaskRepository

from tasks.schemas import TaskSchema, TaskSchemaAdd

from fastapi import HTTPException, status


class TaskService:
    """Encapsulates User logic."""

    def __init__(self, task_repository: TaskRepository):
        """Initialize user service."""
        self._task_repo = task_repository

    async def add(self, author_id: id, data: TaskSchemaAdd):
        new_task = await self._task_repo.add(author_id, data)
        return new_task

    async def get_user_task(self, author_id: id):
        """Process user login."""

        return await self._task_repo.get_user_task(author_id=author_id)
