import json
from fastapi import APIRouter, Depends, HTTPException


from sqlalchemy.ext.asyncio import AsyncSession
from base import get_async_session
from .utils import get_hashed_password
from .models import User
from .schemas import UserCreate

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
async def register_users(
    user: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:

        encrypted_password =get_hashed_password(user.password)

        new_user = User(username=user.username, email=user.email, password=encrypted_password )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return {"message":"user created successfully"}
    except Exception:
        # Передать ошибку разработчикам
        raise HTTPException(
            status_code=500, detail={"status": "error", "data": None, "details": None}
        )




