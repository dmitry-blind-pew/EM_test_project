from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, AdminDep, UserAcsDep
from src.exceptions import ForbiddenException, DataNotFoundException
from src.services.data import DataService

router = APIRouter(prefix="/data", tags=["Данные"])


@router.get("/{data_id}", summary="Получить данные")
async def get_data(data_id: int, chal: UserAcsDep, db: DBDep):
    ttl = 300 if chal > 1 else 60

    @cache(expire=ttl)
    async def get_data_cached(data_id: int, chal: int):
        data = await DataService(db).get_data(data_id)
        if data is None:
            raise DataNotFoundException()
        if data.security_level > chal:
            raise ForbiddenException()
        return data.content

    return await get_data_cached(data_id, chal)


@router.post("", summary="Добавление информации")
async def create_data(new_data: str, access_level: int, al: AdminDep, db: DBDep):
    await DataService(db).create_data(new_data, access_level)
    return {"status": "data_created"}
