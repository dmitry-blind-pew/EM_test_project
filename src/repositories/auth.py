from sqlalchemy import select

from src.mappers.auth import UsersMapperHashed, UsersMapper, UsersActiveMapper, UserAccessLevelsMapper
from src.models.auth import UsersORM
from src.repositories.base import BaseRepository
from pydantic import EmailStr


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UsersMapper

    async def get_deactivate(self):
        is_active = {"is_active": False}
        return UsersActiveMapper.schema.model_validate(is_active)

    async def get_default_access_level(self, user_id: int):
        default_access_level = {"user_id": user_id, "access_level_id": 1}
        return UserAccessLevelsMapper.schema.model_validate(default_access_level)

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model_orm = result.scalars().one_or_none()
        if model_orm is None:
            return None
        return UsersMapperHashed.map_to_domain_entity(model_orm)
