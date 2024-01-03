from auth.repositories.user import UserRepository
from auth.repositories.token import TokenRepository
from auth.schemas import UserCreate, requestdetails
from auth.utils import (
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    verify_password,
)
from fastapi import HTTPException, status, Depends
from dependencies.token import JWTBearer
import config
import jwt


class UserService:
    """Encapsulates User logic."""

    def __init__(
        self, user_repository: UserRepository, token_repository: TokenRepository
    ):
        """Initialize user service."""
        self._user_repo = user_repository
        self._token_repo = token_repository

    async def signup(self, data: UserCreate):
        data.password = get_hashed_password(data.password)

        created_user = await self._user_repo.create(data)
        return created_user

    async def login(self, data: requestdetails):
        """Process user login."""

        return await self._process_login(data=data)

    async def _process_login(self, data: requestdetails):
        user = await self._user_repo.get_by_email(data.email)

        hashed_pass = user.password
        if not verify_password(data.password, hashed_pass):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
            )

        access = create_access_token(user.id)
        refresh = create_refresh_token(user.id)
        token = await self._token_repo.create(
            {
                "user_id": user.id,
                "access_toke": access,
                "refresh_toke": refresh,
                "status": True,
            }
        )

        return token

    async def decode_user_jwt(
        self, token: str, secret_key: str = config.JWT_SECRET_KEY
    ) -> int:
        """Decode access token."""
        try:
            payload = jwt.decode(token, secret_key, algorithms=[config.ALGORITHM])
        except Exception:
            raise HTTPException(
                status_code=403, detail="Invalid token or expired token."
            )
        user_id = payload["sub"]

        return user_id

    async def decode_user_refresh_jwt(self, token: str) -> int:
        """Decode refresh token."""
        try:
            payload = jwt.decode(
                token, config.JWT_REFRESH_SECRET_KEY, algorithms=[config.ALGORITHM]
            )

        except Exception:
            raise HTTPException(
                status_code=403, detail="Invalid token or expired token."
            )
        user_id = payload["sub"]

        return user_id
