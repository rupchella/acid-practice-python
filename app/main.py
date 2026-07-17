from collections.abc import AsyncIterator

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers import accounts

from app.core.config import get_settings

from app.infrastructure.db.pool import create_connection_pool


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()

    db_pool = create_connection_pool(settings)
    db_pool.open()
    app.state.db_pool = db_pool

    try:
        yield
    finally:
        db_pool.close()


app = FastAPI(
    title="ACID Practice Python",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "ACID Practice Python API"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(accounts.router)