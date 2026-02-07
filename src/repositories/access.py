from src.models import AccessLevelsORM
from src.repositories.base import BaseRepository


class AccessRepository(BaseRepository):
    model = AccessLevelsORM
