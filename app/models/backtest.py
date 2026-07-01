from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Backtest(Base):
    __tablename__ = "backtests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    strategy_name: Mapped[str] = mapped_column(String(50), nullable=False)
    pair: Mapped[str] = mapped_column(String(7), nullable=False)
    timeframe: Mapped[str] = mapped_column(String(4), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    initial_balance: Mapped[float] = mapped_column(Float, nullable=False)
    final_balance: Mapped[float] = mapped_column(Float, nullable=False)
    trades_taken: Mapped[int] = mapped_column(Integer, nullable=False)
    win_rate: Mapped[float] = mapped_column(Float, nullable=False)
    profitable: Mapped[bool] = mapped_column(Boolean, nullable=False)
