from tasks.repositories.task import TaskRepository
from .task import TaskService
from sqlalchemy.ext.asyncio import AsyncSession


def provide_task_service(session: AsyncSession) -> TaskService:
    """Providing Task service."""
    task_repository = TaskRepository(session)
    service = TaskService(task_repository)
    return service
