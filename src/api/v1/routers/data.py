from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.deps import DBDep, AdminDep, UserAcsDep
from src.services.data import DataService

router = APIRouter()


@router.get("/{data_id}", summary="Получить данные")
@cache(expire=60)
async def get_data(data_id: int, chal: UserAcsDep, db: DBDep) -> str:
    return await DataService(db).get_allowed_data_content(data_id=data_id, user_access_level=chal)


@router.post("", summary="Добавление информации")
async def create_data(content: str, access_level: int, al: AdminDep, db: DBDep) -> dict[str, str]:
    await DataService(db).create_data(content, access_level)
    return {"status": "data_created"}
