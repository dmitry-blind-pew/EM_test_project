from src.services.base import BaseService


class AdminService(BaseService):
    async def get_users(self, **kwargs):
        return await self.db.admin.get_filtered(**kwargs)

    async def change_access(self, user_id: int, access_level_id: int):
        access_level = await self.db.admin.access_level_patch(access_level_id=access_level_id)
        await self.db.admin.edit(update_data=access_level, exclude_unset=True, user_id=user_id)
        await self.db.commit()
