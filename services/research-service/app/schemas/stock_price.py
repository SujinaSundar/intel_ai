"""
Schemas for stock price data.
"""

from datetime import date

from pydantic import BaseModel, Field


class StockPriceCreate(BaseModel):
    """
    Request model for creating
    stock price data.
    """

    company_id: int = Field(
        description="Company identifier."
    )

    trade_date: date = Field(
        description="Trading date."
    )

    open_price: float = Field(
        description="Opening stock price."
    )

    high_price: float = Field(
        description="Highest stock price."
    )

    low_price: float = Field(
        description="Lowest stock price."
    )

    close_price: float = Field(
        description="Closing stock price."
    )

    volume: int = Field(
        description="Trading volume."
    )


class StockPriceResponse(BaseModel):
    """
    Response model for
    stock price data.
    """

    id: int = Field(
        description="Stock price record identifier."
    )

    company_id: int = Field(
        description="Company identifier."
    )

    trade_date: date = Field(
        description="Trading date."
    )

    open_price: float = Field(
        description="Opening stock price."
    )

    high_price: float = Field(
        description="Highest stock price."
    )

    low_price: float = Field(
        description="Lowest stock price."
    )

    close_price: float = Field(
        description="Closing stock price."
    )

    volume: int = Field(
        description="Trading volume."
    )

    model_config = {
        "from_attributes": True,
    }