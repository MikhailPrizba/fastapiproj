from sqlalchemy.ext.asyncio import AsyncSession
from auth.schemas import TokenCreate
from auth.models import TokenTable


class TokenRepository:
    model = TokenTable
    create_scheme = TokenCreate

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, input_data: create_scheme) -> model:
        token = self.model(**input_data)
        self._session.add(token)
        await self._session.commit()
        await self._session.refresh(token)
        return token
