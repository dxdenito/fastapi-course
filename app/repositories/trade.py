from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trade import Trade
from app.schemas.trade import TradeCreate


class TradeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 10) -> list[Trade]:
        result = await self.db.execute(select(Trade).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_by_id(self, trade_id: int) -> Trade | None:
        result = await self.db.execute(select(Trade).where(Trade.id == trade_id))
        return result.scalar_one_or_none()

    async def create(self, trade: TradeCreate) -> Trade:
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
        self.db.add(db_trade)
        await self.db.flush()
        return db_trade

    async def delete(self, trade: Trade) -> None:
        await self.db.delete(trade)
