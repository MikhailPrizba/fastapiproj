from base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable = False)
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255),nullable = False)
