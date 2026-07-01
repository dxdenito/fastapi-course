from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import Base, engine
from app.models import (
    trade,  # noqa: F401 - imported for side effects (model registration)
)
from app.routers import backtest, positions, products, trades


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(
    title="FastAPI Course",
    description="Learning FastAPI via Claude Course",
    lifespan=lifespan,
)


app.include_router(trades.router)
app.include_router(positions.router)
app.include_router(products.router)
app.include_router(backtest.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Course"}


@app.get("/info")
def get_info():
    return {
        "framework": "FastAPI",
        "python_version": "3.14.6",
        "developer": "Denis Kibathi Karanja",
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}
