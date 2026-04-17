from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.deps import DBDep, AdminDep, UserAcsDep
from src.services.data import DataService

router = APIRouter()


@router.get(
    "/{data_id}",
    summary="Получить данные",
    description="Возвращает содержимое данных с проверкой уровня доступа пользователя.",
)
@cache(expire=60)
async def get_data(*, data_id: int, chal: UserAcsDep, db: DBDep) -> str:
    """Возвращает контент, доступный текущему пользователю."""
    return await DataService(db=db).get_allowed_data_content(data_id=data_id, user_access_level=chal)


@router.post(
    "",
    summary="Добавление информации",
    description="Создает новую запись данных с указанным уровнем доступа. (доступно только администратору)",
)
async def create_data(*, content: str, access_level: int, al: AdminDep, db: DBDep) -> dict[str, str]:
    """Создает запись данных с указанным уровнем доступа."""
    await DataService(db=db).create_data(content=content, access_level=access_level)
    return {"status": "data_created"}
