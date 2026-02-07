from src.services.base import BaseService


class AdminService(BaseService):
    async def get_users(self, **kwargs):
        return await self.db.admin.get_filtered(**kwargs)

    async def change_access(self, id: int, level: int):
        access_level = await self.db.admin.get_is_activate(level=level)
        await self.db.admin.edit(update_data=access_level, exclude_unset=True, user_id=id)
        await self.db.commit()
