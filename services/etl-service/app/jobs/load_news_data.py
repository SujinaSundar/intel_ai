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

import logging
from datetime import datetime

import requests

from app.database.connection import SessionLocal
from app.database.config import settings
from app.database.models import (
    Company,
    NewsMetadata
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

    "Axis Bank": "AXISBANK"

}


def main():

    db = SessionLocal()

    try:

        companies = db.query(
            Company
        ).all()

        logger.info(
            "Found %s companies",
            len(companies)
        )

        for company in companies:

            logger.info(
                "Loading news for %s",
                company.company_name
            )

            try:

                symbol = MARKETAUX_SYMBOLS.get(

                    company.company_name,

                    company.ticker
                    .split(".")[0]
                    .upper()

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
                    timeout=30
                )

                response.raise_for_status()

                data = response.json()

                articles = data.get(
                    "data",
                    []
                )

                logger.info(
                    "Found %s articles",
                    len(articles)
                )

                stored = 0

                for article in articles:

                    # ---------------------------------
                    # Validate company entity
                    # ---------------------------------

                    entities = article.get(
                        "entities",
                        []
                    )

                    found = False

                    for entity in entities:

                        entity_symbol = (
                            entity.get(
                                "symbol",
                                ""
                            )
                            .upper()
                        )

                        if entity_symbol == symbol.upper():

                            found = True

                            break

                    if not found:

                        continue

                    title = article.get(
                        "title"
                    )

                    source = article.get(
                        "source"
                    )

                    article_url = article.get(
                        "url"
                    )

                    published_date = article.get(
                        "published_at"
                    )

                    if not all([

                        title,

                        source,

                        article_url,

                        published_date

                    ]):

                        continue

                    try:

                        published_date = (
                            datetime.fromisoformat(
                                published_date.replace(
                                    "Z",
                                    "+00:00"
                                )
                            )
                        )

                    except Exception:

                        logger.warning(
                            "Invalid date: %s",
                            title
                        )

                        continue

                    # ---------------------------------
                    # Duplicate Check
                    # ---------------------------------

                    existing = (
                        db.query(NewsMetadata).filter(
                            (NewsMetadata.title == title) |
                            (NewsMetadata.url == article_url)
                        )
                        .first()
                    )
                    if existing:

                        continue

                    # ---------------------------------
                    # Store News
                    # ---------------------------------

                    news = NewsMetadata(

                        company_id=company.id,

                        title=title,

                        source=source,

                        url=article_url,

                        published_date=published_date

                    )

                    db.add(
                        news
                    )

                    stored += 1

                logger.info(
                    "%s articles stored for %s",
                    stored,
                    company.company_name
                )

            except Exception:

                logger.exception(
                    "Failed for %s",
                    company.company_name
                )

        db.commit()

        logger.info(
            "News ingestion completed successfully."
        )

    finally:

        db.close()

        logger.info(
            "Database session closed."
        )


if __name__ == "__main__":

    main()