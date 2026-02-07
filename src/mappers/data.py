from src.mappers.base import DataMapper
from src.models import DataORM
from src.schemas.data import DataAddSchema


class DataContentMapper(DataMapper):
    db_model = DataORM
    schema = DataAddSchema
