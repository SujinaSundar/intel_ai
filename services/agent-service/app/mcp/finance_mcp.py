"""
Finance MCP.

Provides stock market retrieval tools
for the Trading Research Agent.
"""

import logging
from datetime import date
from typing import Any

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import (
    Company,
    StockPrice,
)
from app.exceptions.custom_exceptions import (
    CompanyNotFoundException,
    DatabaseException,
    InvalidRequestException,
)

logger = logging.getLogger(__name__)


class FinanceMCP:
    """
    Finance MCP.

    Provides database access methods for
    retrieving stock market information.
    """

    def __init__(self) -> None:
        """
        Initialize Finance MCP.

        A new SQLAlchemy session is created
        for every request.
        """
        pass

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _get_company(
        self,
        db: Session,
        company_name: str,
    ) -> Company:
        """
        Retrieve a company by name.

        Parameters
        ----------
        db : Session
            SQLAlchemy database session.

        company_name : str
            Company name.

        Returns
        -------
        Company
            Matching company.

        Raises
        ------
        InvalidRequestException
            If company name is empty.

        CompanyNotFoundException
            If company does not exist.

        DatabaseException
            If a database error occurs.
        """

        if not company_name or not company_name.strip():
            logger.warning("Empty company name received.")

            raise InvalidRequestException(
                "Company name cannot be empty."
            )

        logger.info(
            "Searching company | company=%s",
            company_name,
        )

        try:

            company = (
                db.query(Company)
                .filter(
                    func.lower(Company.company_name)
                    == company_name.lower()
                )
                .first()
            )

            if company is None:

                logger.warning(
                    "Company not found | company=%s",
                    company_name,
                )

                raise CompanyNotFoundException(
                    company_name
                )

            logger.info(
                "Company found | company=%s",
                company.company_name,
            )

            return company

        except CompanyNotFoundException:
            raise

        except SQLAlchemyError as error:

            logger.exception(
                "Database error while retrieving company."
            )

            raise DatabaseException(
                "Unable to retrieve company information."
            ) from error

    # ---------------------------------------------------------
    # Latest Price
    # ---------------------------------------------------------

    def get_latest_price(
        self,
        company_name: str,
    ) -> dict[str, Any]:
        """
        Retrieve the latest stock price.

        Parameters
        ----------
        company_name : str
            Company name.

        Returns
        -------
        dict[str, Any]
            Latest stock information.

        Raises
        ------
        CompanyNotFoundException
            If company does not exist.

        DatabaseException
            If database query fails.
        """

        logger.info(
            "Fetching latest stock price | company=%s",
            company_name,
        )

        db = SessionLocal()

        try:

            company = self._get_company(
                db,
                company_name,
            )

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

                logger.warning(
                    "No stock data found | company=%s",
                    company_name,
                )

                raise DatabaseException(
                    "No stock data available."
                )

            logger.info(
                "Latest stock retrieved | company=%s",
                company_name,
            )

            return {
                "company": company.company_name,
                "trade_date": latest.trade_date,
                "open": latest.open_price,
                "high": latest.high_price,
                "low": latest.low_price,
                "close": latest.close_price,
                "volume": latest.volume,
            }

        except (
            CompanyNotFoundException,
            InvalidRequestException,
            DatabaseException,
        ):
            raise

        except SQLAlchemyError as error:

            logger.exception(
                "Database error while retrieving latest stock."
            )

            db.rollback()

            raise DatabaseException(
                "Failed to retrieve latest stock price."
            ) from error

        finally:

            db.close()
    # ---------------------------------------------------------
    # Price By Date
    # ---------------------------------------------------------

    def get_price_by_date(
        self,
        company_name: str,
        trade_date: date,
    ) -> dict[str, Any]:
        """
        Retrieve stock price for a specific trading date.

        Parameters
        ----------
        company_name : str
            Company name.

        trade_date : date
            Trading date.

        Returns
        -------
        dict[str, Any]
            Stock price for the requested date.

        Raises
        ------
        InvalidRequestException
            If the trade date is invalid.

        CompanyNotFoundException
            If the company does not exist.

        DatabaseException
            If the database query fails.
        """

        logger.info(
            "Fetching stock price by date | company=%s | trade_date=%s",
            company_name,
            trade_date,
        )

        if trade_date is None:

            logger.warning(
                "Trade date is missing | company=%s",
                company_name,
            )

            raise InvalidRequestException(
                "Trade date cannot be empty."
            )

        db = SessionLocal()

        try:

            company = self._get_company(
                db,
                company_name,
            )

            row = (
                db.query(StockPrice)
                .filter(
                    StockPrice.company_id == company.id,
                    StockPrice.trade_date == trade_date,
                )
                .first()
            )

            if row is None:

                logger.warning(
                    "No stock data found | company=%s | trade_date=%s",
                    company_name,
                    trade_date,
                )

                raise DatabaseException(
                    f"No stock data available for {trade_date}."
                )

            logger.info(
                "Stock price retrieved | company=%s | trade_date=%s",
                company_name,
                trade_date,
            )

            return {
                "company": company.company_name,
                "trade_date": row.trade_date,
                "open": row.open_price,
                "high": row.high_price,
                "low": row.low_price,
                "close": row.close_price,
                "volume": row.volume,
            }

        except (
            InvalidRequestException,
            CompanyNotFoundException,
            DatabaseException,
        ):
            raise

        except SQLAlchemyError as error:

            logger.exception(
                "Database error while retrieving stock by date."
            )

            db.rollback()

            raise DatabaseException(
                "Failed to retrieve stock price."
            ) from error

        finally:

            db.close()

    # ---------------------------------------------------------
    # Price History
    # ---------------------------------------------------------

    def get_price_history(
        self,
        company_name: str,
        limit: int = 30,
    ) -> list[dict[str, Any]]:
        """
        Retrieve historical stock prices.

        Parameters
        ----------
        company_name : str
            Company name.

        limit : int, default=30
            Maximum number of trading days.

        Returns
        -------
        list[dict[str, Any]]
            Historical stock prices ordered by
            descending trade date.

        Raises
        ------
        InvalidRequestException
            If the requested limit is invalid.

        CompanyNotFoundException
            If the company does not exist.

        DatabaseException
            If the database query fails.
        """

        logger.info(
            "Fetching price history | company=%s | limit=%s",
            company_name,
            limit,
        )

        if limit <= 0:

            logger.warning(
                "Invalid history limit | company=%s | limit=%s",
                company_name,
                limit,
            )

            raise InvalidRequestException(
                "History limit must be greater than zero."
            )

        limit = min(limit, 365)

        db = SessionLocal()

        try:

            company = self._get_company(
                db,
                company_name,
            )

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

                logger.warning(
                    "No price history found | company=%s",
                    company_name,
                )

                raise DatabaseException(
                    "No historical stock data available."
                )

            logger.info(
                "Price history retrieved | company=%s | records=%s",
                company_name,
                len(rows),
            )

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

        except (
            InvalidRequestException,
            CompanyNotFoundException,
            DatabaseException,
        ):
            raise

        except SQLAlchemyError as error:

            logger.exception(
                "Database error while retrieving price history."
            )

            db.rollback()

            raise DatabaseException(
                "Failed to retrieve price history."
            ) from error

        finally:

            db.close()
    # ---------------------------------------------------------
    # Latest Volume
    # ---------------------------------------------------------

    def get_latest_volume(
        self,
        company_name: str,
    ) -> dict[str, Any]:
        """
        Retrieve the latest trading volume.

        Parameters
        ----------
        company_name : str
            Company name.

        Returns
        -------
        dict[str, Any]
            Latest trading volume information.

        Raises
        ------
        CompanyNotFoundException
            If the company does not exist.

        DatabaseException
            If the stock data cannot be retrieved.
        """

        logger.info(
            "Fetching latest trading volume | company=%s",
            company_name,
        )

        latest = self.get_latest_price(
            company_name
        )

        logger.info(
            "Latest trading volume retrieved | company=%s",
            company_name,
        )

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
    ) -> dict[str, Any]:
        """
        Retrieve a summary of the latest stock data.

        The summary includes the latest open, high,
        low, close, trading volume, daily price
        change, and percentage change.

        Parameters
        ----------
        company_name : str
            Company name.

        Returns
        -------
        dict[str, Any]
            Stock summary.

        Raises
        ------
        CompanyNotFoundException
            If the company does not exist.

        DatabaseException
            If the latest stock data cannot be retrieved.
        """

        logger.info(
            "Generating stock summary | company=%s",
            company_name,
        )

        latest = self.get_latest_price(
            company_name
        )

        day_change = (
            latest["close"]
            - latest["open"]
        )

        percent_change = 0.0

        if latest["open"] != 0:
            percent_change = (
                day_change
                / latest["open"]
            ) * 100

        summary = {
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

        logger.info(
            "Stock summary generated successfully | company=%s",
            company_name,
        )

        return summary