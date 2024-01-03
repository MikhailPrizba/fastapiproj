import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from .services.services import provide_user_service

from base import get_async_session

from .models import TokenTable, User
from .schemas import TokenCreate, TokenSchema, UserCreate, requestdetails
from .utils import (
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    verify_password,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
async def register_users(
    user: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    service = provide_user_service(session)
    user = await service.signup(user)
    return user


@router.post("/login", response_model=TokenSchema)
async def login(
    request: requestdetails, session: AsyncSession = Depends(get_async_session)
):
    service = provide_user_service(session)
    token = await service.login(request)
    return {
        "access_token": token.access_toke,
        "refresh_token": token.refresh_toke,
    }
