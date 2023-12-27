import json
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from base import get_async_session
from .utils import get_hashed_password, verify_password, create_access_token, create_refresh_token
from .models import User, TokenTable
from .schemas import UserCreate, TokenCreate, TokenSchema, requestdetails

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

@router.post('/login' ,response_model=TokenSchema)
async def login(request: requestdetails, session: AsyncSession = Depends(get_async_session)):
    query = select(User).filter(User.email == request.email)
    result = await session.execute(query)
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    hashed_pass = user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    access=create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    token_db = TokenTable(user_id=user.id,  access_toke=access,  refresh_toke=refresh, status=True)
    session.add(token_db)
    await session.commit()
    await session.refresh(token_db)
    return {
        "access_token": access,
        "refresh_token": refresh,
    }



