from pathlib import Path
import sys
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import router as router_auth
from src.api.data import router as router_data
from src.api.admin import router as router_admin
from src.init import redis_connector


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_connector.connect()
    FastAPICache.init(RedisBackend(redis_connector.redis), prefix="fastapi-cache")
    await redis_connector.ping()
    yield
    await redis_connector.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_data)
app.include_router(router_admin)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
