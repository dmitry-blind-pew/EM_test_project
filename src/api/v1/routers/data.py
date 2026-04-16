from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.deps import DBDep, AdminDep, UserAcsDep
from src.core.exceptions import ForbiddenException, DataNotFoundException
from src.services.data import DataService

router = APIRouter()


@router.get("/{data_id}", summary="Получить данные")
async def get_data(data_id: int, chal: UserAcsDep, db: DBDep):
    ttl = 300 if chal > 1 else 60

    @cache(expire=ttl)
    def get_data_cached(data_id: AllowData):
        return data.content

    return await get_data_cached(data_id, chal)


@router.post("", summary="Добавление информации")
async def create_data(content: str, access_level: int, al: AdminDep, db: DBDep) -> dict[str, str]:
    await DataService(db).create_data(content, access_level)
    return {"status": "data_created"}
