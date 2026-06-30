from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator




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

