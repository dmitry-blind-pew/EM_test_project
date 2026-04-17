from fastapi import APIRouter
from src.api.v1.routers import admin, auth, data


api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(admin.router, prefix="/admin", tags=["Администрирование"])
api_v1_router.include_router(auth.router, prefix="/auth", tags=["Аутентификация и авторизация"])
api_v1_router.include_router(data.router, prefix="/data", tags=["Данные"])
