import uuid
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator, model_validator


class Product(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Product name",
        examples=["Laptop", "Phone"],
    )
    price: float = Field(
        ..., gt=0, description="Price of the product", examples=[35000, 50000]
    )
    stock: int = Field(
        ..., ge=0, description="Number of units in stock", examples=[10, 20]
    )
    description: str | None = Field(
        None, max_length=300, description="Optional product description"
    )
    active: bool = Field(
        True, description="Whether the product is active", examples=[True, False]
    )


class RiskMetrics(BaseModel):
    risk_percent: float = Field(..., gt=0, le=10, description="risk percent")
    risk_reward_ratio: float = Field(..., gt=0, description="risk to reward ratio")
    account_balance: float = Field(..., gt=0, description="account balance > 0")


class TimeFrameAnalysis(BaseModel):
    timeframe: str = Field(
        ...,
        pattern="^(4H|4h|30m|5m|1m)$",
        examples=["4H", "30m", "5m", "1m"],
        description="timeframe selection",
    )
    bias: str = Field(
        ...,
        pattern="^(bullish|bearish|neutral)$",
        examples=["bullish", "bearish", "neutral"],
        description="bias of the market",
    )
    notes: str | None = None


class Trade(BaseModel):
    pair: str = Field(
        ...,
        min_length=6,
        max_length=7,
        description="Currency pair e.g. EURUSD",
        examples=["EURUSD", "GBPJPY"],
    )
    direction: str = Field(
        ...,
        pattern="^(buy|sell)$",
        description="Trade direction",
        examples=["buy", "sell"],
    )
    entry_price: float = Field(
        ..., gt=0, description="Entry price — must be positive", examples=[1.1056]
    )
    stop_loss: float = Field(
        ..., gt=0, description="Stop loss price", examples=[1.1040]
    )
    take_profit: float = Field(
        ..., gt=0, description="Take profit price", examples=[1.1120]
    )
    lot_size: float = Field(
        0.01,
        gt=0,
        le=100,
        description="Position size in lots",
        examples=[0.01, 0.1, 1.0],
    )
    risk: RiskMetrics = Field(..., description="risk metrics for the trade")
    timeframes: list[TimeFrameAnalysis] = Field(
        default_factory=list, description="multi-timeframe analysis"
    )
    notes: str | None = Field(None, max_length=500, description="Optional trade notes")

    @field_validator("pair")
    @classmethod
    def normalize_pair(cls, value):
        value = value.upper()

        if not value.isalpha():
            raise ValueError("Only letters (A-Z) allowed!")
        return value

    @field_validator("direction", mode="before")
    @classmethod
    def normalize_direction(cls, value):
        return value.lower()

    @model_validator(mode="after")
    def check_model(self):
        if self.direction == "buy":
            if self.stop_loss >= self.entry_price:
                raise ValueError("BUY: stoploss must be below the entry price")
            if self.take_profit <= self.entry_price:
                raise ValueError("BUY: take profit must be above the entry price")

        if self.direction == "sell":
            if self.stop_loss <= self.entry_price:
                raise ValueError("SELL: stoploss must be above the entry price")
            if self.take_profit >= self.entry_price:
                raise ValueError("SELL: take profit must be below the entry price")
        return self


class TradeResponse(BaseModel):
    id: str
    pair: str
    direction: str
    entry_price: float
    stop_loss: float
    take_profit: float
    lot_size: float
    logged_at: datetime


app = FastAPI(title="FastAPI Course", description="Learning FastAPI via Claude Course")


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Course"}


@app.get("/info")
def get_info():
    return {
        "framework": "FastAPI",
        "python_version": "3.14.6",
        "developer": "Denis Kibathi Karanja",
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/products/{product_id}")
def get_product(product_id: int):
    return {"id": product_id, "name": "Sample Product"}


@app.get("/search")
def search(query: str, limit: int = 5, active: bool | None = None):
    return {"query": query, "limit": limit, "active": active}


@app.get("/users/{user_id}/orders")
def get_user_orders(user_id: int, status: str | None = None, page: int = 1):
    return {"user_id": user_id, "status": status, "page": page}


@app.post("/products")
def create_product(product: Product):
    return {"product": product, "message": "Product created successfully"}


@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product, notify: bool = False):
    return {"product_id": product_id, "product": product, "notify": notify}


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    return {"message": f"Product {product_id} deleted", "success": True}


# MODULE 1 FINAL TEST ENDPOINTS


@app.get("/trades", response_model=list[TradeResponse])
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


@app.get("/trades/summary")
def get_summary(pair: str | None = None, direction: str | None = None):
    return {"pair": pair, "direction": direction, "total_trades": 0}


@app.get("/trades/{trade_id}")
def get_trade(trade_id: int):
    return {"trade_id": trade_id, "pair": "EURUSD"}


@app.post("/trades", response_model=TradeResponse)
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


@app.delete("/trades/{trade_id}")
def delete_trade(trade_id: int):
    return {"message": f"Trade {trade_id} removed", "success": True}


class PositionRisk(BaseModel):
    max_drawdown_percent: float = Field(..., gt=0, le=100, examples=[3.5, 10, 15])
    account_balance: float = Field(..., gt=0, examples=[2000, 200, 156.56])


class PositionCreate(BaseModel):
    symbol: str = Field(
        ...,
        min_length=3,
        max_length=10,
        description="symbol being traded",
        examples=["EURUSD", "GBPJPY"],
    )
    side: str = Field(
        ...,
        pattern="^(long|short)$",
        description="direction of trade taken",
        examples=["long", "short"],
    )
    entry_price: float = Field(
        ..., gt=0, description="entry price", examples=[1.1025, 2.3434]
    )
    exit_price: float | None = Field(
        None, gt=0, description="optional exit price", examples=[1.2324, 123, 34]
    )
    size: float = Field(..., gt=0, description="lot size", examples=[1, 2, 2.56])
    risk: PositionRisk = Field(..., description="risk assesment")

    @field_validator("symbol")
    @classmethod
    def normalise_symbol(cls, value):
        return value.upper()

    @field_validator("side", mode="before")
    @classmethod
    def normalise_side(cls, value):
        return value.lower()

    @model_validator(mode="after")
    def check_model(self):
        if self.exit_price:
            if self.side == "long":
                if self.exit_price <= self.entry_price:
                    raise ValueError("Long: exit price must be higher than entry price")

            if self.side == "short":
                if self.exit_price >= self.entry_price:
                    raise ValueError("Short: exit price must be lower than entry price")

        return self


class PositionResponse(BaseModel):
    id: str
    symbol: str
    side: str
    entry_price: float
    exit_price: float
    size: float
    opened_at: datetime


@app.post("/positions", response_model=PositionResponse)
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


@app.get("/positions", response_model=list[PositionResponse])
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


@app.get("/positions/{position_id}", response_model=PositionResponse)
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
