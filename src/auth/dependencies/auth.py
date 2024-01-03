from fastapi import Depends
from base import get_async_session

from dependencies.token import JWTBearer
from auth.services.services import provide_user_service
from sqlalchemy.ext.asyncio import AsyncSession


async def get_current_user(
    access_token: str = Depends(JWTBearer()),
    session: AsyncSession = Depends(get_async_session),
) -> int:
    """Return current user."""
    service = provide_user_service(session)
    user_id = await service.decode_user_jwt(access_token)
    return user_id
