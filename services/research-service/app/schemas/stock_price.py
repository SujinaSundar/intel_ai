from datetime import date
from pydantic import BaseModel


class StockPriceCreate(BaseModel):
    company_id: int
    trade_date: date
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int


class StockPriceResponse(BaseModel):
    id: int
    company_id: int
    trade_date: date
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int

    model_config = {
        "from_attributes": True
    }