from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import BaseORM


class DataORM(BaseORM):
    __tablename__ = "data"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]
    security_level: Mapped[int] = mapped_column(default=0)
