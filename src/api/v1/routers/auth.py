from fastapi import APIRouter, Response
from fastapi_cache.decorator import cache

from src.api.deps import UserIdDep, DBDep
from src.schemas.auth import UserRegDataSchema, UserPatchSchema, UserLogDataSchema
from src.services.auth import AuthService


router = APIRouter()


@router.get("/me", summary="Моя информация", description="Возвращает профиль текущего авторизованного пользователя.")
@cache(expire=30)
async def get_me(*, user_id: UserIdDep, db: DBDep):
    """Возвращает профиль текущего пользователя."""
    user = await AuthService(db=db).get_me(user_id=user_id)
    return user


@router.post(
    "/register",
    summary="Регистрация клиента",
    description="Создает нового пользователя, с базовым уровнем доступа.",
)
async def register_user(*, user_data: UserRegDataSchema, db: DBDep):
    """Регистрирует нового пользователя."""
    await AuthService(db=db).register_user(user_data=user_data)
    return {"status": "User Registered"}


@router.post(
    "/login",
    summary="Аутентификация клиента",
    description="Проверяет учетные данные и авторизует клиента.",
)
async def login_user(*, user_data: UserLogDataSchema, response: Response, db: DBDep):
    """Аутентифицирует пользователя и пробрасывает токен доступа в куки."""
    access_token = await AuthService(db=db).login_user(user_data=user_data)
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/logout", summary="Выход из системы", description="Завершает пользовательскую сессию.")
async def logout_user(*, response: Response):
    """Завершает сессию текущего пользователя."""
    response.delete_cookie("access_token")
    return {"status": "User Logged Out"}


@router.patch(
    "/me", summary="Редактирование профиля", description="Частично обновляет данные профиля текущего пользователя."
)
async def edit_user(*, user_id: UserIdDep, user_data: UserPatchSchema, db: DBDep):
    """Редактирует профиль текущего пользователя."""
    await AuthService(db=db).patch_user(user_id=user_id, user_data=user_data)
    return {"status": "User Edited"}


@router.delete("/me", summary="Удалить профиль", description="Деактивирует текущего пользователя.")
async def delete_user(*, response: Response, user_id: UserIdDep, db: DBDep):
    """Деактивирует аккаунт текущего пользователя."""
    await AuthService(db=db).delete_user(user_id=user_id)
    response.delete_cookie("access_token")
    return {"status": "User deleted"}
