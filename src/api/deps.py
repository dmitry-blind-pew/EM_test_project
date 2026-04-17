from typing import Annotated
import logging
from fastapi import Depends, Request

from src.core.db import async_session_maker
from src.core.exceptions import UnauthorizedException, ForbiddenException
from src.services.auth import AuthService
from src.utils.db_manager import DBManager

logger = logging.getLogger(__name__)


def get_access_token(*, request: Request) -> str:
    """Читает токена доступа из кук."""
    access_token = request.cookies.get("access_token", None)
    if not access_token:
        logger.warning("Access token не найден в cookies")
        raise UnauthorizedException()
    return access_token


def get_current_user_id(*, access_token: str = Depends(get_access_token)) -> int:
    """Извлекает id пользователя из токена доступа."""
    user_token_data = AuthService().decode_access_token(token=access_token)
    return user_token_data["user_id"]


def get_current_access_level(*, access_token: str = Depends(get_access_token)) -> int:
    """Извлекает уровень доступа из токена доступа."""
    user_token_data = AuthService().decode_access_token(token=access_token)
    return user_token_data["access_level_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]
UserAcsDep = Annotated[int, Depends(get_current_access_level)]


def require_admin(*, al: UserAcsDep) -> int:
    """Разрешает доступ только администраторам."""
    if al != 3:
        logger.warning("Доступ к admin endpoint запрещен. access_level=%s", al)
        raise ForbiddenException()
    return al


AdminDep = Annotated[int, Depends(require_admin)]


async def get_db():
    """Возвращает менеджер БД через dependency."""
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
