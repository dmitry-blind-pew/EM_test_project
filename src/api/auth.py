from fastapi import APIRouter, Response
from fastapi_cache.decorator import cache

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.auth import UserRegDataSchema, UserPatchSchema, UserLogDataSchema
from src.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.get("/me", summary="Моя информация")
@cache(expire=30)
async def get_me(user_id: UserIdDep, db: DBDep):
    user = await AuthService(db).get_me(user_id=user_id)
    return user


@router.post("/register", summary="Регистрация клиента")
async def register_user(user_data: UserRegDataSchema, db: DBDep):
    await AuthService(db).register_user(user_data)
    return {"status": "User Registered"}


@router.post("/login", summary="Аутентификация клиента")
async def login_user(user_data: UserLogDataSchema, response: Response, db: DBDep):
    access_token = await AuthService(db).login_user(user_data)
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/logout", summary="Выход из системы")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "User Logged Out"}


@router.patch("/me", summary="Редактирование профиля")
async def edit_user(user_id: UserIdDep, user_data: UserPatchSchema, db: DBDep):
    await AuthService(db).patch_user(user_id, user_data)
    return {"status": "User Edited"}


@router.delete("/me", summary="Удалить профиль")
async def delete_user(response: Response, user_id: UserIdDep, db: DBDep):
    await AuthService(db).delete_user(user_id=user_id)
    response.delete_cookie("access_token")
    return {"status": "User deleted"}
