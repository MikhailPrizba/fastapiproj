from sqlalchemy import delete, desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from typing import Union
from auth.schemas import UserCreate
from auth.models import User

class UserRepository:
    
    model = User  # type: ignore
    create_scheme = UserCreate  # type: ignore
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def create(self, input_data: create_scheme) -> model:
        user = self.model(**input_data.model_dump())
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user
    @staticmethod
    def check_object(obj: model) -> Union[bool, HTTPException]:
        """Check if object exist."""
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email"
        )
        return True
    
    async def retrieve(self, pk: id) -> User:
        res = await self._session.execute(select(self.model).where(self.model.id == pk))
        user = res.scalars().first()
        self.check_object(user)
        await self._session.refresh(user)
        return user
    
    async def get_by_email(self, email: str) -> User:
        res = await self._session.execute(
            select(self.model).where(self.model.email == email) # noqa
        )
        user = res.scalars().first()
        self.check_object(user)
        return user
