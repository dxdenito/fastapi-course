from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, pagination_params
from app.repositories.trade import TradeRepository
from app.schemas.trade import TradeCreate, TradeResponse

router = APIRouter(prefix="/trades", tags=["trades"])


# app/routers/trades.py — cleaned up
@router.get("/", response_model=list[TradeResponse])
async def get_trades(
    pagination: dict = Depends(pagination_params), db: AsyncSession = Depends(get_db)
):
    repo = TradeRepository(db)
    return await repo.get_all(skip=pagination["skip"], limit=pagination["limit"])


@router.post("/", response_model=TradeResponse)
async def create_trade(trade: TradeCreate, db: AsyncSession = Depends(get_db)):
    repo = TradeRepository(db)
    return await repo.create(trade)


@router.get("/{trade_id}", response_model=TradeResponse)
async def get_trade(trade_id: int, db: AsyncSession = Depends(get_db)):
    repo = TradeRepository(db)
    trade = await repo.get_by_id(trade_id)
    if trade is None:
        raise HTTPException(status_code=404, detail=f"Trade {trade_id} not found")
    return trade


@router.delete("/{trade_id}")
async def delete_trade(trade_id: int, db: AsyncSession = Depends(get_db)):
    repo = TradeRepository(db)
    trade = await repo.get_by_id(trade_id)
    if trade is None:
        raise HTTPException(status_code=404, detail=f"Trade {trade_id} not found")
    await repo.delete(trade)
    return {"message": f"Trade {trade_id} deleted", "success": True}
