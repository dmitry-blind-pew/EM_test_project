from src.mappers.data import DataContentMapper
from src.models import DataORM
from src.repositories.base import BaseRepository


class DataRepository(BaseRepository):
    model = DataORM
    mapper = DataContentMapper

    async def create_new_data(self, new_data: str, access_level: int):
        new_data_stmt = {"content": new_data, "security_level": access_level}
        return self.mapper.schema.model_validate(new_data_stmt)
