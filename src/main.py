from pathlib import Path
import sys
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

from src.api.v1.router import api_v1_router
from src.core.redis_connector import redis_connector


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_connector.connect()
    FastAPICache.init(RedisBackend(redis_connector.redis), prefix="fastapi-cache")
    await redis_connector.ping()
    yield
    await redis_connector.disconnect()


app = FastAPI(
    title="EM Project",
    description="## Система аутентификации и авторизации",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Dmitry (Telegram)",
        "url": "https://t.me/dmitry_kartab",
    },
    lifespan=lifespan,
)

app.include_router(api_v1_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
