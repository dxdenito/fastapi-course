from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, pagination_params, verify_api_key
from app.repositories.backtest import BacktestRepository
from app.schemas.backtest import BacktestCreate, BacktestResponse

router = APIRouter(
    prefix="/backtest", tags=["backtests"], dependencies=[Depends(verify_api_key)]
)


@router.post("/", response_model=BacktestResponse)
async def create_backtest(backtest: BacktestCreate, db: AsyncSession = Depends(get_db)):

    wins = round((backtest.win_rate / 100) * backtest.trades_taken)
    losses = backtest.trades_taken - wins

    # assuming compound calculation i.e risk based on starting balance not compounding
    # wins is 2% (0.02) and loss 1%(0.01) gains
    final_balance = backtest.initial_balance
    final_balance += (backtest.initial_balance * 0.02) * wins
    final_balance -= (backtest.initial_balance * 0.01) * losses

    profitable = final_balance > backtest.initial_balance

    repo = BacktestRepository(db)
    return await repo.create(backtest, final_balance, profitable)


@router.get("/", response_model=list[BacktestResponse])
async def get_backtests(
    pagination: dict = Depends(pagination_params), db: AsyncSession = Depends(get_db)
):
    repo = BacktestRepository(db)
    return await repo.get_all(skip=pagination["skip"], limit=pagination["limit"])


@router.get("/{backtest_id}", response_model=BacktestResponse)
async def get_backtest(backtest_id: int, db: AsyncSession = Depends(get_db)):
    repo = BacktestRepository(db)
    backtest = await repo.get_by_id(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found!")
    return backtest


@router.delete("/{backtest_id}")
async def delete_backtest(backtest_id: int, db: AsyncSession = Depends(get_db)):
    repo = BacktestRepository(db)
    backtest = await repo.get_by_id(backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found!")
    await repo.delete(backtest)
    return {"message": "Backtest Successfully deleted"}
