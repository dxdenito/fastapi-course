import uuid
from datetime import datetime

from fastapi import APIRouter

from app.schemas.trade import Trade, TradeResponse

router = APIRouter(prefix="/trades", tags=["trades"])


@router.get("/", response_model=list[TradeResponse])
def get_trades():
    return [
        {
            "id": str(uuid.uuid4()),
            "pair": "EURUSD",
            "direction": "buy",
            "entry_price": 1.1056,
            "stop_loss": 1.1046,
            "take_profit": 1.2546,
            "lot_size": 2,
            "notes": "I am feeling positive and I followed my rules",
            "logged_at": datetime.now(),
        },
        {
            "id": str(uuid.uuid4()),
            "pair": "EURJPY",
            "direction": "sell",
            "entry_price": 156.105,
            "stop_loss": 156.200,
            "take_profit": 145.254,
            "lot_size": 2,
            "notes": "I am not feeling confident but I followed my rules",
            "logged_at": datetime.now(),
        },
    ]


@router.get("/summary")
def get_summary(pair: str | None = None, direction: str | None = None):
    return {"pair": pair, "direction": direction, "total_trades": 0}


@router.get("/{trade_id}")
def get_trade(trade_id: int):
    return {"trade_id": trade_id, "pair": "EURUSD"}


@router.post("/", response_model=TradeResponse)
def log_trade(trade: Trade):
    return {
        "id": str(uuid.uuid4()),
        "pair": trade.pair,
        "direction": trade.direction,
        "entry_price": trade.entry_price,
        "stop_loss": trade.stop_loss,
        "take_profit": trade.take_profit,
        "lot_size": trade.lot_size,
        "logged_at": datetime.now(),
    }


@router.delete("/{trade_id}")
def delete_trade(trade_id: int):
    return {"message": f"Trade {trade_id} removed", "success": True}
