from sqlalchemy import insert, select, update
from pydantic import BaseModel

from src.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, limit: int | None = None, offset: int = 0, **filter_by) -> list:
        """Возвращает список сущностей по фильтрам."""
        if offset < 0:
            raise ValueError("offset must be greater than or equal to 0")
        if limit is not None and limit <= 0:
            raise ValueError("limit must be greater than 0")
        query = select(self.model).filter(*filter).filter_by(**filter_by).limit(limit).offset(offset)
        result = await self.session.execute(query)
        model_orm = result.scalars().all()
        return [self.mapper.map_to_domain_entity(model) for model in model_orm]

    async def add(self, data: BaseModel):
        """Добавляет одну сущность."""
        add_data_statement = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_statement)
        model_orm = result.scalars().one()
        return self.mapper.map_to_domain_entity(model_orm)

    async def add_bulk(self, data: list[BaseModel]) -> None:
        """Добавляет список сущностей."""
        if not data:
            return
        add_data_statement = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_statement)

    async def get_one_or_none(self, **filter_by):
        """Возвращает одну сущность или None по фильтрам."""
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model_orm = result.scalars().one_or_none()
        if model_orm is None:
            return None
        return self.mapper.map_to_domain_entity(model_orm)

    async def edit(self, update_data: BaseModel, exclude_unset: bool = False, **filter_by):
        """Обновляет сущности по фильтрам."""
        update_data_statement = (
            update(self.model).filter_by(**filter_by).values(update_data.model_dump(exclude_unset=exclude_unset))
        )
        return await self.session.execute(update_data_statement)
