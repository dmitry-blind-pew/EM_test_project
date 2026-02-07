from src.services.base import BaseService


class DataService(BaseService):
    async def get_data(self, data_id: int):
        return await self.db.data.get_one_or_none(id=data_id)

    async def create_data(self, new_data: str, access_level: int):
        data_stmt = await self.db.data.create_new_data(new_data=new_data, access_level=access_level)
        await self.db.data.add(data_stmt)
        await self.db.commit()
