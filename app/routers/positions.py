import uuid
from datetime import datetime

from fastapi import APIRouter

from app.schemas.position import PositionCreate, PositionResponse

router = APIRouter(prefix="/positions", tags=["positions"])


@router.post("/", response_model=PositionResponse)
def create_position(position: PositionCreate):
    return {
        "id": str(uuid.uuid4()),
        "symbol": position.symbol,
        "side": position.side,
        "entry_price": position.entry_price,
        "exit_price": position.exit_price,
        "size": position.size,
        "opened_at": datetime.now(),
    }


@router.get("/", response_model=list[PositionResponse])
def get_positions():
    return [
        {
            "id": str(uuid.uuid4()),
            "symbol": "EURUSD",
            "side": "long",
            "entry_price": 1.1056,
            "exit_price": 1.2545,
            "size": 1.5,
            "opened_at": datetime.now(),
        },
        {
            "id": str(uuid.uuid4()),
            "symbol": "GBPJPY",
            "side": "long",
            "entry_price": 126.10,
            "exit_price": 135.25,
            "size": 1.5,
            "opened_at": datetime.now(),
        },
    ]


@router.get("/{position_id}", response_model=PositionResponse)
def get_position(position_id: int):
    return {
        "id": str(position_id),
        "symbol": "GBPJPY",
        "side": "long",
        "entry_price": 126.10,
        "exit_price": 135.25,
        "size": 1.5,
        "opened_at": datetime.now(),
    }
