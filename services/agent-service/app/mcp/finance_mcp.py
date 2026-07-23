"""
Finance MCP

Provides stock market tools
for the Trading Research Agent.
"""

from datetime import date

from sqlalchemy import func

from app.database.connection import SessionLocal
from app.database.models import (
    Company,
    StockPrice,
)


class FinanceMCP:
    """
    Finance MCP.

    Provides stock market
    retrieval tools.
    """

    def __init__(self):
        """
        No persistent database session.

        A new SQLAlchemy session is
        created for every request.
        """
        pass

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _get_company(
    self,
    db,
    company_name: str,
):
        """
        Retrieve company by name.
        """

        print("=" * 60)
        print("LOOKING FOR COMPANY:", repr(company_name))
        print("=" * 60)

        company = (
            db.query(Company)
            .filter(
                func.lower(Company.company_name)
                == company_name.lower()
            )
            .first()
        )

        print("FOUND:", company.company_name if company else None)

        return company

    # ---------------------------------------------------------
    # Latest Price
    # ---------------------------------------------------------

    def get_latest_price(
        self,
        company_name: str,
    ):

        db = SessionLocal()

        try:

            company = self._get_company(
                db,
                company_name,
            )

            if company is None:

                return {
                    "error": "Company not found"
                }

            latest = (
                db.query(StockPrice)
                .filter(
                    StockPrice.company_id == company.id
                )
                .order_by(
                    StockPrice.trade_date.desc()
                )
                .first()
            )

            if latest is None:

                return {
                    "error": "No stock data found"
                }

            return {

                "company": company.company_name,

                "trade_date": latest.trade_date,

                "open": latest.open_price,

                "high": latest.high_price,

                "low": latest.low_price,

                "close": latest.close_price,

                "volume": latest.volume,

            }

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()

    # ---------------------------------------------------------
    # Price By Date
    # ---------------------------------------------------------

    def get_price_by_date(
        self,
        company_name: str,
        trade_date: date,
    ):

        db = SessionLocal()

        try:

            company = self._get_company(
                db,
                company_name,
            )

            if company is None:

                return {
                    "error": "Company not found"
                }

            row = (
                db.query(StockPrice)
                .filter(
                    StockPrice.company_id == company.id,
                    StockPrice.trade_date == trade_date,
                )
                .first()
            )

            if row is None:

                return {
                    "error": f"No stock data available for {trade_date}"
                }

            return {

                "company": company.company_name,

                "trade_date": row.trade_date,

                "open": row.open_price,

                "high": row.high_price,

                "low": row.low_price,

                "close": row.close_price,

                "volume": row.volume,

            }

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()

    # ---------------------------------------------------------
    # Price History
    # ---------------------------------------------------------

    def get_price_history(
        self,
        company_name: str,
        limit: int = 30,
    ):

        db = SessionLocal()

        try:

            company = self._get_company(
                db,
                company_name,
            )

            if company is None:

                return {
                    "error": "Company not found"
                }

            if limit is None:
                limit = 30

            limit = max(1, min(limit, 365))

            rows = (
                db.query(StockPrice)
                .filter(
                    StockPrice.company_id == company.id
                )
                .order_by(
                    StockPrice.trade_date.desc()
                )
                .limit(limit)
                .all()
            )

            if not rows:

                return {
                    "error": "No stock data found"
                }

            return [

                {

                    "date": row.trade_date,

                    "open": row.open_price,

                    "high": row.high_price,

                    "low": row.low_price,

                    "close": row.close_price,

                    "volume": row.volume,

                }

                for row in rows

            ]

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()

    # ---------------------------------------------------------
    # Latest Volume
    # ---------------------------------------------------------

    def get_latest_volume(
        self,
        company_name: str,
    ):

        latest = self.get_latest_price(
            company_name
        )

        if "error" in latest:

            return latest

        return {

            "company": latest["company"],

            "trade_date": latest["trade_date"],

            "volume": latest["volume"],

        }

    # ---------------------------------------------------------
    # Stock Summary
    # ---------------------------------------------------------

    def get_stock_summary(
        self,
        company_name: str,
    ):

        latest = self.get_latest_price(
            company_name
        )

        if "error" in latest:

            return latest

        day_change = (
            latest["close"]
            - latest["open"]
        )

        percent_change = 0

        if latest["open"] != 0:

            percent_change = (
                day_change
                / latest["open"]
            ) * 100

        return {

            "company": latest["company"],

            "trade_date": latest["trade_date"],

            "open": latest["open"],

            "close": latest["close"],

            "high": latest["high"],

            "low": latest["low"],

            "volume": latest["volume"],

            "day_change": round(
                day_change,
                2,
            ),

            "percent_change": round(
                percent_change,
                2,
            ),

        }