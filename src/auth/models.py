import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255), nullable=False)


class TokenTable(Base):
    __tablename__ = "token"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    access_toke: Mapped[str] = mapped_column(String(450), unique=True, nullable=False)
    refresh_toke: Mapped[str] = mapped_column(String(450), unique=True, nullable=False)
    status: Mapped[bool]
    created_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now()
    )
