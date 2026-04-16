from src.services.base import BaseService
from src.core.exceptions import DataNotFoundException, ForbiddenException


class DataService(BaseService):
    async def get_data(self, data_id: int):
        return await self.db.data.get_one_or_none(id=data_id)

    async def get_allowed_data_content(self, data_id: int, user_access_level: int) -> str:
        data = await self.get_data(data_id)
        if data is None:
            raise DataNotFoundException()
        if data.security_level > user_access_level:
            raise ForbiddenException()
        return data.content

    async def create_data(self, content: str, access_level: int):
        data_stmt = await self.db.data.create_new_data(new_data=content, access_level=access_level)
        await self.db.data.add(data_stmt)
        await self.db.commit()
