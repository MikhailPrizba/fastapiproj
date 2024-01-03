from auth.repositories.user import UserRepository
from auth.repositories.token import TokenRepository
from .user import UserService
from sqlalchemy.ext.asyncio import AsyncSession


def provide_user_service(session: AsyncSession) -> UserService:
    """Providing user service."""
    user_repository = UserRepository(session)
    token_repository = TokenRepository(session)
    service = UserService(user_repository, token_repository)
    return service
