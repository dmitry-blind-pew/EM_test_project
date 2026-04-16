from fastapi import APIRouter

from src.api.deps import DBDep, AdminDep
from src.services.admin import AdminService


router = APIRouter()


@router.get("/users", summary="Информация о пользователях")
async def get_users(user_id: int, al: AdminDep, db: DBDep) -> list:
    return await AdminService(db).get_users(user_id=user_id)


@router.put("/users/roles", summary="Редактировать права доступа")
async def change_access_level(user_id: int, access_level: int, al: AdminDep, db: DBDep) -> dict[str, str]:
    await AdminService(db).change_access(user_id=user_id, access_level_id=access_level)
    return {"status": "access_level_changed"}
