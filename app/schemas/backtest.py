from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator


class BacktestRisk(BaseModel):
    risk_percent: float = Field(..., gt=0, le=10)
    max_consecutive_losses: int = Field(..., le=20, ge=1)


class BacktestCreate(BaseModel):
    strategy_name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Stategy name",
        examples=["ORB Strategy"],
    )
    pair: str = Field(
        ...,
        min_length=6,
        max_length=7,
        description="pair tested",
        examples=["EURUSD", "GBPJPY"],
    )
    timeframe: str = Field(
        ...,
        pattern="^(4h|4H|30m|5m|1m)$",
        description="timeframe used for backtesting",
        examples=["4H", "30m"],
    )
    start_date: datetime
    end_date: datetime
    initial_balance: float = Field(..., gt=0)
    risk: BacktestRisk = Field(..., description="risk assesment")
    trades_taken: int = Field(
        ..., ge=0, description="how many trades occured in the backtest"
    )
    win_rate: float = Field(..., ge=0, le=100)

    @field_validator("pair")
    @classmethod
    def normalise_pair(cls, value):
        value = value.upper()

        if not value.isalpha():
            raise ValueError("Only letters (A-Z) allowed!")
        return value

    @model_validator(mode="after")
    def check_model(self):
        if self.end_date < self.start_date:
            raise ValueError("End date must be later than start date")
        return self


class BacktestResponse(BaseModel):
    id: str
    strategy_name: str
    pair: str
    timeframe: str
    start_date: datetime
    end_date: datetime
    initial_balance: float
    final_balance: float
    trades_taken: int
    win_rate: float
    profitable: bool
