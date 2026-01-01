from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.settings import app_settings, fast_api_settings
from config.db import init_db
from auth.routers import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    **fast_api_settings.model_dump(),
    debug=app_settings.debug,
    lifespan=lifespan,
)


# routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
