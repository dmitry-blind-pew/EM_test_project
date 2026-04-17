# ruff: noqa: E402
import json
from typing import AsyncGenerator
from unittest import mock

from src.api.deps import get_db
from src.schemas.access import AccessLevelsSchema
from src.schemas.data import DataAddSchema
from src.services.auth import AuthService

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest
from httpx import ASGITransport, AsyncClient

from src.core.config import settings
from src.core.db import BaseORM, async_session_maker_null_pool, engine_null_pool
from src.main import app
from src.models import *  # noqa
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    """Проверяет, что тесты запущены в тестовом режиме."""
    assert settings.MODE == "TEST"


async def get_db_manager_null_pool():
    """Возвращает DBManager с ограниченным до одного пулом соединений."""
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db_manager() -> AsyncGenerator[DBManager, None]:
    """Предоставляет DBManager для теста."""
    async for db in get_db_manager_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_manager_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    """Подготавливает и наполняет тестовую базу начальными данными."""
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(BaseORM.metadata.drop_all)
        await conn.run_sync(BaseORM.metadata.create_all)
    with (
        open("tests/data_test/mock_access_levels.json", "r", encoding="utf-8") as access_levels_file,
        open("tests/data_test/mock_data.json", "r", encoding="utf-8") as data_content_file,
    ):
        access_levels_data = json.load(access_levels_file)
        data_content_data = json.load(data_content_file)
    access_levels_schemas = [AccessLevelsSchema.model_validate(level) for level in access_levels_data]
    data_content_schemas = [DataAddSchema.model_validate(data_content) for data_content in data_content_data]
    async for db in get_db_manager_null_pool():
        await db.access.add_bulk(access_levels_schemas)
        await db.data.add_bulk(data_content_schemas)
        await db.commit()


@pytest.fixture(scope="session")
async def async_client():
    """Создает HTTP-клиент."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as aclient:
        yield aclient


@pytest.fixture(scope="session", autouse=True)
async def create_user(async_client, setup_database):
    """Создает базового пользователя для auth-сценариев."""
    await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@gmail.com",
            "password": "1234",
            "first_name": "Fixture",
            "password_repeat": "1234",
        },
    )


@pytest.fixture(scope="session")
async def auth_async_client(create_user, async_client):
    """Возвращает авторизованный HTTP-клиент."""
    await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@gmail.com",
            "password": "1234",
        },
    )
    assert async_client.cookies["access_token"]
    yield async_client


@pytest.fixture
def all_tokens(setup_database):
    """Возвращает набор JWT токенов для ролей в тестах."""
    auth_service = AuthService()
    return {
        "none": None,
        "user": auth_service.create_access_token(data={"user_id": 5, "access_level_id": 1}),
        "premium": auth_service.create_access_token(data={"user_id": 6, "access_level_id": 2}),
        "admin": auth_service.create_access_token(data={"user_id": 7, "access_level_id": 3}),
    }
