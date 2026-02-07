from typing import Annotated
from fastapi import Depends, Request

from src.database import async_session_maker
from src.exceptions import UnauthorizedException, ForbiddenException
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


def get_access_token(request: Request) -> str:
    access_token = request.cookies.get("access_token", None)
    if not access_token:
        raise UnauthorizedException()
    return access_token


def get_current_user_id(access_token: str = Depends(get_access_token)) -> int:
    user_token_data = AuthService().decode_access_token(access_token)
    return user_token_data["user_id"]


def get_current_access_level(access_token: str = Depends(get_access_token)) -> int:
    user_token_data = AuthService().decode_access_token(access_token)
    return user_token_data["access_level_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]
UserAcsDep = Annotated[int, Depends(get_current_access_level)]


def require_admin(al: UserAcsDep) -> int:
    if al != 3:
        raise ForbiddenException()
    return al


AdminDep = Annotated[int, Depends(require_admin)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
