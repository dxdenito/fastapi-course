from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, pagination_params
from app.models.trade import Trade
from app.schemas.trade import TradeCreate, TradeResponse

router = APIRouter(prefix="/trades", tags=["trades"])


@router.get("/summary")
async def get_summary(pair: str | None = None, direction: str | None = None):
    return {"pair": pair, "direction": direction, "total_trades": 0}


@router.get("/", response_model=list[TradeResponse])
async def get_trades(
    pagination: dict = Depends(pagination_params), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Trade).offset(pagination["skip"]).limit(pagination["limit"])
    )
    return result.scalars().all()


@router.get("/{trade_id}", response_model=TradeResponse)
async def get_trade(trade_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trade).where(Trade.id == trade_id))
    trade = result.scalar_one_or_none()
    if trade is None:
        raise HTTPException(status_code=404, detail=f"Trade {trade_id} not found")
    return trade


@router.post("/", response_model=TradeResponse)
async def create_trade(trade: TradeCreate, db: AsyncSession = Depends(get_db)):
    db_trade = Trade(
        pair=trade.pair,
        direction=trade.direction,
        entry_price=trade.entry_price,
        stop_loss=trade.stop_loss,
        take_profit=trade.take_profit,
        lot_size=trade.lot_size,
        notes=trade.notes,
        logged_at=datetime.now(),
    )
    db.add(db_trade)
    await db.flush()
    return db_trade


@router.delete("/{trade_id}")
async def delete_trade(trade_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trade).where(Trade.id == trade_id))
    trade = result.scalar_one_or_none()
    if trade is None:
        raise HTTPException(status_code=404, detail=f"Trade {trade_id} not found")
    await db.delete(trade)
    return {"message": f"Trade {trade_id} deleted", "success": True}
