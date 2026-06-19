"""
Stock Data Ingestion Job

Purpose:
--------
This job performs the Stock ETL pipeline.

ETL Steps:
----------
1. Extract stock data from Yahoo Finance.
2. Validate incoming stock data.
3. Remove duplicate records.
4. Transform the data into the application schema.
5. Load the data into PostgreSQL.

Data Validation:
----------------
- Open price must not be null.
- High price must not be null.
- Low price must not be null.
- Close price must not be null.
- Volume must not be negative.

Duplicate Removal:
------------------
- A company can have only one stock record per trade date.
- Duplicate records are skipped before insertion.
"""

import logging

import pandas as pd
import yfinance as yf

from app.database.connection import SessionLocal
from app.database.models import Company
from app.database.models import StockPrice


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """
    Main entry point for stock data ingestion.
    """

    db = SessionLocal()

    try:

        companies = db.query(Company).all()

        logger.info("Found %s companies", len(companies))

        for company in companies:

            logger.info(
                "Loading stock data for %s",
                company.company_name
            )

            try:

                ticker = yf.Ticker(company.ticker)

                # Extract
                data = ticker.history(period="5d")

                if data.empty:

                    logger.warning(
                        "No stock data found for %s",
                        company.company_name
                    )

                    continue

                for index, row in data.iterrows():

                    # -------------------------
                    # Data Validation
                    # -------------------------

                    if pd.isna(row["Open"]):
                        continue

                    if pd.isna(row["High"]):
                        continue

                    if pd.isna(row["Low"]):
                        continue

                    if pd.isna(row["Close"]):
                        continue

                    if pd.isna(row["Volume"]):
                        continue

                    if row["Volume"] < 0:
                        continue

                    # -------------------------
                    # Duplicate Removal
                    # -------------------------

                    existing = (
                        db.query(StockPrice)
                        .filter(
                            StockPrice.company_id == company.id,
                            StockPrice.trade_date == index.date()
                        )
                        .first()
                    )

                    if existing:
                        continue

                    # -------------------------
                    # Transform
                    # -------------------------

                    stock = StockPrice(
                        company_id=company.id,
                        trade_date=index.date(),
                        open_price=float(row["Open"]),
                        high_price=float(row["High"]),
                        low_price=float(row["Low"]),
                        close_price=float(row["Close"]),
                        volume=int(row["Volume"])
                    )

                    # -------------------------
                    # Load
                    # -------------------------

                    db.add(stock)

                logger.info(
                    "Stock data stored for %s",
                    company.company_name
                )

            except Exception as exc:

                logger.error(
                    "Failed for %s: %s",
                    company.company_name,
                    exc
                )

        db.commit()

        logger.info(
            "Stock data ingestion completed successfully"
        )

    finally:

        db.close()

        logger.info(
            "Database session closed"
        )


if __name__ == "__main__":
    main()
