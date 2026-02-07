from sqlalchemy import select

from src.mappers.auth import UserAccessLevelsMapper, UserAccessLevelsPatchMapper
from src.models import UserAccessLevelsORM
from src.repositories.base import BaseRepository


class AdminRepository(BaseRepository):
    model = UserAccessLevelsORM
    mapper = UserAccessLevelsMapper

    async def get_is_activate(self, level: int):
        access_level = {"access_level_id": level}
        return UserAccessLevelsPatchMapper.schema.model_validate(access_level)

    async def get_user_access_level_id(self, user_id: int):
        query = select(self.model).filter_by(user_id=user_id)
        result = await self.session.execute(query)
        model_orm = result.scalars().one()
        return self.mapper.map_to_domain_entity(model_orm)
