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
"""

import pandas as pd
import yfinance as yf
from app.core.logger import logger
from app.database.connection import SessionLocal
from app.database.models import Company, StockPrice


def main():
    """Main entry point for stock data ingestion."""

    logger.info("=" * 80)
    logger.info("Starting Stock Data Ingestion Job")
    logger.info("=" * 80)

    db = SessionLocal()

    total_records = 0

    try:

        companies = db.query(Company).all()

        logger.info(
            "Found %d companies for stock ingestion",
            len(companies),
        )

        for company in companies:

            logger.info(
                "Processing company: %s",
                company.company_name,
            )

            try:

                logger.info(
                    "Fetching stock data from Yahoo Finance for %s (%s)",
                    company.company_name,
                    company.ticker,
                )

                ticker = yf.Ticker(company.ticker)

                data = ticker.history(period="5d")

                if data.empty:

                    logger.warning(
                        "No stock data found for %s",
                        company.company_name,
                    )

                    continue

                logger.info(
                    "Yahoo Finance returned %d records",
                    len(data),
                )

                stored = 0

                for index, row in data.iterrows():

                    # -------------------------
                    # Data Validation
                    # -------------------------

                    if any(
                        pd.isna(row[col])
                        for col in ["Open", "High", "Low", "Close", "Volume"]
                    ):
                        logger.debug(
                            "Skipping record for %s due to missing values",
                            index.date(),
                        )
                        continue

                    if row["Volume"] < 0:
                        logger.warning(
                            "Skipping record with negative volume for %s",
                            index.date(),
                        )
                        continue

                    # -------------------------
                    # Duplicate Check
                    # -------------------------

                    existing = (
                        db.query(StockPrice)
                        .filter(
                            StockPrice.company_id == company.id,
                            StockPrice.trade_date == index.date(),
                        )
                        .first()
                    )

                    if existing:
                        logger.debug(
                            "Duplicate stock record skipped for %s on %s",
                            company.company_name,
                            index.date(),
                        )
                        continue

                    # -------------------------
                    # Transform & Load
                    # -------------------------

                    stock = StockPrice(
                        company_id=company.id,
                        trade_date=index.date(),
                        open_price=float(row["Open"]),
                        high_price=float(row["High"]),
                        low_price=float(row["Low"]),
                        close_price=float(row["Close"]),
                        volume=int(row["Volume"]),
                    )

                    db.add(stock)

                    stored += 1

                db.commit()

                total_records += stored

                logger.info(
                    "%d stock records stored for %s",
                    stored,
                    company.company_name,
                )

            except Exception:

                db.rollback()

                logger.exception(
                    "Stock ingestion failed for company: %s",
                    company.company_name,
                )

        logger.info("=" * 80)
        logger.info("Stock ETL Summary")
        logger.info("Companies Processed : %d", len(companies))
        logger.info("Total Records Stored : %d", total_records)
        logger.info("Stock Data Ingestion Completed Successfully")
        logger.info("=" * 80)

    except Exception:

        db.rollback()

        logger.exception("Stock ETL pipeline failed.")

        raise

    finally:

        db.close()

        logger.info("Database session closed.")


if __name__ == "__main__":
    main()