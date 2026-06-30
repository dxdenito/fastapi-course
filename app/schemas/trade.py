from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator


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
