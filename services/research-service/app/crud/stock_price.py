"""
CRUD operations for StockPrice.
"""

from datetime import date

from app.database.models import StockPrice
from sqlalchemy.orm import Session


class StockPriceCRUD:
    """
    Handles all StockPrice database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_latest(self, company_id: int):
        """
        Retrieve the latest available stock price for a company.
        """

        return (
            self.db.query(StockPrice)
            .filter(
                StockPrice.company_id == company_id
            )
            .order_by(
                StockPrice.trade_date.desc()
            )
            .first()
        )

    def get_history(
        self,
        company_id: int,
        limit: int = 30
    ):
        """
        Retrieve recent stock price history.
        """

        return (
            self.db.query(StockPrice)
            .filter(
                StockPrice.company_id == company_id
            )
            .order_by(
                StockPrice.trade_date.desc()
            )
            .limit(limit)
            .all()
        )

    def get_by_date(
        self,
        company_id: int,
        trade_date: date
    ):
        """
        Retrieve stock price for a specific date.
        """

        return (
            self.db.query(StockPrice)
            .filter(
                StockPrice.company_id == company_id,
                StockPrice.trade_date == trade_date
            )
            .first()
        )

    def get_between_dates(
        self,
        company_id: int,
        start_date: date,
        end_date: date
    ):
        """
        Retrieve stock prices between two dates.
        """

        return (
            self.db.query(StockPrice)
            .filter(
                StockPrice.company_id == company_id,
                StockPrice.trade_date >= start_date,
                StockPrice.trade_date <= end_date
            )
            .order_by(
                StockPrice.trade_date.asc()
            )
            .all()
        )