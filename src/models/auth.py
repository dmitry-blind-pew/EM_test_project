import typing
from typing import List
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import BaseORM


if typing.TYPE_CHECKING:
    from src.models import AccessLevelsORM


class UsersORM(BaseORM):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str | None] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    access_levels: Mapped[List["AccessLevelsORM"]] = relationship(
        secondary="user_access_levels", back_populates="users"
    )
