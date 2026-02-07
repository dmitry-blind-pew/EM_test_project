import typing
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import BaseORM


if typing.TYPE_CHECKING:
    from src.models import UsersORM


class AccessLevelsORM(BaseORM):
    __tablename__ = "access_levels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    users: Mapped[List["UsersORM"]] = relationship(secondary="user_access_levels", back_populates="access_levels")


class UserAccessLevelsORM(BaseORM):
    __tablename__ = "user_access_levels"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    access_level_id: Mapped[int] = mapped_column(ForeignKey("access_levels.id"))
