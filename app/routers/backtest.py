import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import pagination_params, verify_api_key
from app.schemas.backtest import BacktestCreate, BacktestResponse

router = APIRouter(
    prefix="/backtest", tags=["backtests"], dependencies=[Depends(verify_api_key)]
)


@router.post("/", response_model=BacktestResponse)
def create_backtest(backtest: BacktestCreate):
    wins = round((backtest.win_rate / 100) * backtest.trades_taken)
    losses = backtest.trades_taken - wins

    # assuming compound calculation i.e risk based on starting balance not compounding
    # wins is 2% (0.02) and loss 1%(0.01) gains
    final_balance = backtest.initial_balance
    final_balance += (backtest.initial_balance * 0.02) * wins
    final_balance -= (backtest.initial_balance * 0.01) * losses

    profitable = final_balance > backtest.initial_balance

    return {
        "id": str(uuid.uuid4()),
        "strategy_name": backtest.strategy_name,
        "pair": backtest.pair,
        "timeframe": backtest.timeframe,
        "start_date": backtest.start_date,
        "end_date": backtest.end_date,
        "initial_balance": backtest.initial_balance,
        "final_balance": final_balance,
        "trades_taken": backtest.trades_taken,
        "win_rate": backtest.win_rate,
        "profitable": profitable,
    }


@router.get("/", response_model=list[BacktestResponse])
def get_backtests(pagination: dict = Depends(pagination_params)):
    skip = pagination["skip"]
    limit = pagination["limit"]
    print(f"skip is: {skip} and limit is: {limit}")

    return [
        {
            "id": str(uuid.uuid4()),
            "strategy_name": "ICT 2022 MODEL",
            "pair": "GBPJPY",
            "timeframe": "4H",
            "start_date": "2026-06-30T14:22:14.176000Z",
            "end_date": "2026-07-30T14:22:14.176000Z",
            "initial_balance": 100,
            "final_balance": 1500,
            "trades_taken": 1000,
            "win_rate": 80,
            "profitable": True,
        },
        {
            "id": str(uuid.uuid4()),
            "strategy_name": "ECCENTRIC LIQUIDATION",
            "pair": "XAUUSD",
            "timeframe": "4H",
            "start_date": "2026-09-30T14:22:14.176000Z",
            "end_date": "2026-11-30T14:22:14.176000Z",
            "initial_balance": 1000,
            "final_balance": 15000,
            "trades_taken": 1000,
            "win_rate": 80,
            "profitable": True,
        },
    ]


@router.get("/{backtest_id}", response_model=BacktestResponse)
def get_backtest(backtest_id: int):
    if backtest_id != 1:
        raise HTTPException(status_code=404, detail="Backtest not found!")
    return {
        "id": str(backtest_id),
        "strategy_name": "ALC CONCEPT",
        "pair": "AUDUSD",
        "timeframe": "4H",
        "start_date": "2026-09-30T14:22:14.176000Z",
        "end_date": "2026-11-30T14:22:14.176000Z",
        "initial_balance": 2000,
        "final_balance": 30000,
        "trades_taken": 1000,
        "win_rate": 80,
        "profitable": True,
    }


@router.delete("/{backtest_id}")
def delete_backtest(backtest_id: int):
    if backtest_id != 1:
        raise HTTPException(status_code=404, detail="Backtest not found!")

    return {"message": "Backtest Successfully deleted"}
