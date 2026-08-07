"""
News Data Ingestion Job

Purpose:
--------
This job performs the News ETL pipeline.

ETL Steps:
----------
1. Extract news articles from Marketaux.
2. Validate incoming news data.
3. Verify company entity.
4. Remove duplicate records.
5. Transform the data into the application schema.
6. Load the data into PostgreSQL.
"""

from datetime import datetime

import requests
from app.core.logger import logger
from app.database.config import settings
from app.database.connection import SessionLocal
from app.database.models import Company, NewsMetadata

# --------------------------------------------------
# Marketaux Symbol Mapping
# --------------------------------------------------

MARKETAUX_SYMBOLS = {
    "Reliance Industries": "RELIANCE",
    "TCS": "TCS.NS",
    "Infosys": "INFY",
    "HDFC Bank": "HDFCBANK",
    "ICICI Bank": "ICICIBANK",
    "Bharti Airtel": "BHARTIARTL",
    "ITC": "ITC",
    "Larsen & Toubro": "LT",
    "State Bank of India": "SBIN",
    "Axis Bank": "AXISBANK",
}


def main():

    logger.info("=" * 80)
    logger.info("Starting News Data Ingestion Job")
    logger.info("=" * 80)

    db = SessionLocal()

    total_articles = 0

    try:

        companies = db.query(Company).all()

        logger.info(
            "Found %d companies for news ingestion",
            len(companies),
        )

        for company in companies:

            logger.info(
                "Processing company: %s",
                company.company_name,
            )

            try:

                symbol = MARKETAUX_SYMBOLS.get(
                    company.company_name,
                    company.ticker.split(".")[0].upper(),
                )

                logger.info(
                    "Fetching news from Marketaux for %s (%s)",
                    company.company_name,
                    symbol,
                )

                url = (
                    "https://api.marketaux.com/v1/news/all"
                    f"?symbols={symbol}"
                    "&filter_entities=true"
                    "&language=en"
                    "&limit=20"
                    f"&api_token={settings.MARKETAUX_API_KEY}"
                )

                response = requests.get(
                    url,
                    timeout=30,
                )

                response.raise_for_status()

                data = response.json()

                articles = data.get("data", [])

                logger.info(
                    "Marketaux returned %d articles",
                    len(articles),
                )

                stored = 0

                for article in articles:

                    entities = article.get("entities", [])

                    found = False

                    for entity in entities:

                        entity_symbol = entity.get(
                            "symbol",
                            "",
                        ).upper()

                        if entity_symbol == symbol.upper():
                            found = True
                            break

                    if not found:
                        logger.debug(
                            "Skipping article because company entity was not found."
                        )
                        continue

                    title = article.get("title")
                    source = article.get("source")
                    article_url = article.get("url")
                    published_date = article.get("published_at")

                    if not all(
                        [
                            title,
                            source,
                            article_url,
                            published_date,
                        ]
                    ):
                        logger.warning(
                            "Skipping article due to missing required fields."
                        )
                        continue

                    try:

                        published_date = datetime.fromisoformat(
                            published_date.replace(
                                "Z",
                                "+00:00",
                            )
                        )

                    except Exception:

                        logger.warning(
                            "Invalid published date for article: %s",
                            title,
                        )

                        continue

                    existing = (
                        db.query(NewsMetadata)
                        .filter(
                            (NewsMetadata.title == title)
                            | (NewsMetadata.url == article_url)
                        )
                        .first()
                    )

                    if existing:
                        logger.debug(
                            "Duplicate article skipped: %s",
                            title,
                        )
                        continue

                    news = NewsMetadata(
                        company_id=company.id,
                        title=title,
                        source=source,
                        url=article_url,
                        published_date=published_date,
                    )

                    db.add(news)

                    stored += 1

                db.commit()

                total_articles += stored

                logger.info(
                    "%d articles stored for %s",
                    stored,
                    company.company_name,
                )

            except Exception:

                db.rollback()

                logger.exception(
                    "News ingestion failed for company: %s",
                    company.company_name,
                )

        logger.info("=" * 80)
        logger.info("News ETL Summary")
        logger.info("Companies Processed : %d", len(companies))
        logger.info("Total Articles Stored : %d", total_articles)
        logger.info("News Data Ingestion Completed Successfully")
        logger.info("=" * 80)

    except Exception:

        db.rollback()

        logger.exception(
            "News ETL pipeline failed."
        )

        raise

    finally:

        db.close()

        logger.info("Database session closed.")


if __name__ == "__main__":
    main()