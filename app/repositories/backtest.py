from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.backtest import Backtest
from app.schemas.backtest import BacktestCreate


class BacktestRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 10) -> list[Backtest]:
        result = await self.db.execute(select(Backtest).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_by_id(self, backtest_id: int) -> Backtest | None:
        result = await self.db.execute(
            select(Backtest).where(Backtest.id == backtest_id)
        )
        return result.scalar_one_or_none()

    async def create(
        self, backtest: BacktestCreate, final_balance: float, profitable: bool
    ) -> Backtest:
        db_backtest = Backtest(
            strategy_name=backtest.strategy_name,
            pair=backtest.pair,
            timeframe=backtest.timeframe,
            start_date=backtest.start_date,
            end_date=backtest.end_date,
            initial_balance=backtest.initial_balance,
            final_balance=final_balance,
            trades_taken=backtest.trades_taken,
            win_rate=backtest.win_rate,
            profitable=profitable,
        )
        self.db.add(db_backtest)
        await self.db.flush()
        return db_backtest

    async def delete(self, backtest: Backtest) -> None:
        await self.db.delete(backtest)
