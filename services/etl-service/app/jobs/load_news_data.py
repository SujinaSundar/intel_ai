
"""
News Data Ingestion Job

Purpose:
--------
This job performs the News ETL pipeline.

ETL Steps:
----------
1. Extract news articles from Alpha Vantage.
2. Validate incoming news data.
3. Remove duplicate records.
4. Transform the data into the application schema.
5. Load the data into PostgreSQL.

Data Validation:
----------------
- Title must not be empty.
- URL must not be empty.
- Source must not be empty.
- Published date must not be empty.

Duplicate Removal:
------------------
- News URL must be unique.
- Duplicate articles are skipped before insertion.
"""

import logging
from datetime import datetime

import requests

from app.database.connection import SessionLocal
from app.database.config import settings
from app.database.models import Company
from app.database.models import NewsMetadata


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():

    db = SessionLocal()

    try:

        companies = db.query(Company).all()

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

                url = (
                    "https://www.alphavantage.co/query"
                    "?function=NEWS_SENTIMENT"
                    f"&keywords={company.company_name}"
                    f"&apikey={settings.ALPHA_VANTAGE_API_KEY}"
                )

                logger.info(
                    "Calling API for %s",
                    company.company_name
                )

                response = requests.get(
                    url,
                    timeout=30
                )

                logger.info(
                    "API response received"
                )

                data = response.json()

                articles = data.get(
                    "feed",
                    []
                )

                logger.info(
                    "Found %s articles",
                    len(articles)
                )

                for article in articles:

                    # -------------------------
                    # Data Validation
                    # -------------------------

                    title = article.get("title")
                    source = article.get("source")
                    article_url = article.get("url")
                    published_date = article.get(
                        "time_published"
                    )

                    if not title:
                        continue

                    if not source:
                        continue

                    if not article_url:
                        continue

                    if not published_date:
                        continue

                    # -------------------------
                    # Convert Date
                    # -------------------------

                    try:

                        published_date = datetime.strptime(
                            published_date,
                            "%Y%m%dT%H%M%S"
                        )

                    except Exception:

                        logger.warning(
                            "Invalid date format for article: %s",
                            title
                        )

                        continue

                    # -------------------------
                    # Duplicate Removal
                    # -------------------------

                    existing_news = (
                        db.query(NewsMetadata)
                        .filter(
                            NewsMetadata.url
                            == article_url
                        )
                        .first()
                    )

                    if existing_news:
                        continue

                    # -------------------------
                    # Transform + Load
                    # -------------------------

                    news = NewsMetadata(
                        company_id=company.id,
                        title=title,
                        source=source,
                        url=article_url,
                        published_date=published_date
                    )

                    db.add(news)

                logger.info(
                    "News stored for %s",
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
            "News ingestion completed successfully"
        )

    finally:

        db.close()

        logger.info(
            "Database session closed"
        )


if __name__ == "__main__":
    main()
