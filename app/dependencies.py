from typing import AsyncGenerator

from fastapi import Header, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal


def pagination_params(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    return {"skip": skip, "limit": limit}


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != "steezyfx-secret-2026":
        raise HTTPException(status_code=401, detail="Invalid API key")

    return


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
