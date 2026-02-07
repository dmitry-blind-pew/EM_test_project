from fastapi import APIRouter

from src.api.dependencies import DBDep, AdminDep
from src.services.admin import AdminService


router = APIRouter(prefix="/admin", tags=["Администрирование"])


@router.get("/users", summary="Информация о пользователях")
async def get_users(user_id: int, al: AdminDep, db: DBDep):
    return await AdminService(db).get_users(user_id=user_id)


@router.put("/users/roles", summary="Редактировать права доступа")
async def change_access_level(user_id: int, access_level: int, al: AdminDep, db: DBDep):
    await AdminService(db).change_access(id=user_id, level=access_level)
    return {"status": "access_level_changed"}
