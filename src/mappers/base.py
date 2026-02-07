from typing import TypeVar, Type, Generic
from pydantic import BaseModel

from src.database import BaseORM

ModelType = TypeVar("ModelType", bound=BaseORM)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper(Generic[ModelType, SchemaType]):
    model_ORM: Type[ModelType]
    schema: Type[SchemaType]

    @classmethod
    def map_to_domain_entity(cls, model_data: ModelType) -> SchemaType:
        return cls.schema.model_validate(model_data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, schema_data: SchemaType) -> ModelType:
        return cls.model_ORM(**schema_data.model_dump())
