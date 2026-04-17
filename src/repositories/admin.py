from sqlalchemy import select

from src.mappers.auth import UserAccessLevelsMapper, UserAccessLevelsPatchMapper
from src.models import UserAccessLevelsORM
from src.repositories.base import BaseRepository


class AdminRepository(BaseRepository):
    model = UserAccessLevelsORM
    mapper = UserAccessLevelsMapper

    async def access_level_patch(self, *, access_level_id: int):
        """Формирует схему патча для обновления уровня доступа."""
        access_level = {"access_level_id": access_level_id}
        return UserAccessLevelsPatchMapper.schema.model_validate(access_level)

    async def get_user_access_level_id(self, *, user_id: int):
        """Получает текущую запись уровня доступа пользователя."""
        query = select(self.model).filter_by(user_id=user_id)
        result = await self.session.execute(query)
        model_orm = result.scalars().one_or_none()
        if model_orm is None:
            return None
        return self.mapper.map_to_domain_entity(model_orm)
