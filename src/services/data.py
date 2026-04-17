from src.services.base import BaseService
from src.core.exceptions import DataNotFoundException, ForbiddenException
import logging

logger = logging.getLogger(__name__)


class DataService(BaseService):
    async def get_data(self, *, data_id: int):
        """Выгружает данные по id."""
        return await self.db.data.get_one_or_none(id=data_id)

    async def get_allowed_data_content(self, *, data_id: int, user_access_level: int) -> str:
        """Возвращает данные, если уровень доступа пользователя это позволяет."""
        data = await self.get_data(data_id=data_id)
        if data is None:
            logger.warning("Данные не найдены data_id=%s", data_id)
            raise DataNotFoundException()
        if data.security_level > user_access_level:
            logger.warning(
                "Доступ к данным запрещен data_id=%s required_level=%s user_level=%s",
                data_id,
                data.security_level,
                user_access_level,
            )
            raise ForbiddenException()
        return data.content

    async def create_data(self, *, content: str, access_level: int):
        """Создает новую запись с данными."""
        data_stmt = await self.db.data.create_new_data(new_data=content, access_level=access_level)
        await self.db.data.add(data_stmt)
        await self.db.commit()
