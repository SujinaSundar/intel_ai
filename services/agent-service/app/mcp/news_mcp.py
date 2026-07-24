"""
News MCP.

Provides news retrieval tools
for the Trading Research Agent.
"""

import logging
from typing import Any

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import (
    Company,
    NewsMetadata,
    SentimentScore,
)
from app.exceptions.custom_exceptions import (
    CompanyNotFoundException,
    DatabaseException,
    InvalidRequestException,
)

logger = logging.getLogger(__name__)


class NewsMCP:
    """
    News MCP.

    Provides news retrieval
    tools for company news
    and sentiment analysis.
    """

    def __init__(self) -> None:
        """
        Initialize News MCP.

        A new SQLAlchemy session is
        created for every request.
        """
        pass

    # -----------------------------------------------------
    # Private Helper
    # -----------------------------------------------------

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
            If the company name is empty.

        CompanyNotFoundException
            If the company does not exist.

        DatabaseException
            If a database error occurs.
        """

        if not company_name or not company_name.strip():

            logger.warning(
                "Empty company name received."
            )

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
                    func.lower(
                        Company.company_name
                    )
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
                "Unable to retrieve company."
            ) from error

    # -----------------------------------------------------
    # Latest News
    # -----------------------------------------------------

    def get_latest_news(
        self,
        company_name: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Retrieve the latest company news.

        Parameters
        ----------
        company_name : str
            Company name.

        limit : int
            Maximum number of
            news articles.

        Returns
        -------
        list[dict[str, Any]]
            Latest company news.

        Raises
        ------
        InvalidRequestException
            If limit is invalid.

        CompanyNotFoundException
            If company does not exist.

        DatabaseException
            If database query fails.
        """

        logger.info(
            "Fetching latest news | company=%s | limit=%s",
            company_name,
            limit,
        )

        if limit <= 0:

            logger.warning(
                "Invalid news limit | company=%s | limit=%s",
                company_name,
                limit,
            )

            raise InvalidRequestException(
                "Limit must be greater than zero."
            )

        limit = min(limit, 100)

        db = SessionLocal()

        try:

            company = self._get_company(
                db,
                company_name,
            )

            rows = (
                db.query(
                    NewsMetadata,
                    SentimentScore,
                )
                .outerjoin(
                    SentimentScore,
                    NewsMetadata.id
                    == SentimentScore.news_id,
                )
                .filter(
                    NewsMetadata.company_id
                    == company.id
                )
                .order_by(
                    NewsMetadata.published_date.desc()
                )
                .limit(limit)
                .all()
            )

            logger.info(
                "Retrieved %s news articles | company=%s",
                len(rows),
                company_name,
            )

            return [
                {
                    "title": news.title,
                    "source": news.source,
                    "published_date": news.published_date,
                    "url": news.url,
                    "sentiment": (
                        sentiment.sentiment_label
                        if sentiment
                        else "Not Available"
                    ),
                    "confidence": (
                        round(
                            sentiment.confidence_score * 100,
                            2,
                        )
                        if sentiment
                        else None
                    ),
                }
                for news, sentiment in rows
            ]

        except (
            InvalidRequestException,
            CompanyNotFoundException,
            DatabaseException,
        ):
            raise

        except SQLAlchemyError as error:

            logger.exception(
                "Database error while retrieving latest news."
            )

            db.rollback()

            raise DatabaseException(
                "Failed to retrieve latest news."
            ) from error

        finally:

            db.close()
    # -----------------------------------------------------
    # Company News
    # -----------------------------------------------------

    def get_company_news(
        self,
        company_name: str,
    ) -> list[dict[str, Any]]:
        """
        Retrieve the latest company news.

        Parameters
        ----------
        company_name : str
            Company name.

        Returns
        -------
        list[dict[str, Any]]
            Latest company news.
        """

        logger.info(
            "Fetching company news | company=%s",
            company_name,
        )

        return self.get_latest_news(
            company_name=company_name,
            limit=10,
        )

    # -----------------------------------------------------
    # Latest Sentiment
    # -----------------------------------------------------

    def get_latest_sentiment(
        self,
        company_name: str,
    ) -> dict[str, Any]:
        """
        Retrieve the latest sentiment
        for a company.

        Parameters
        ----------
        company_name : str
            Company name.

        Returns
        -------
        dict[str, Any]
            Latest sentiment information.

        Raises
        ------
        CompanyNotFoundException
            If company does not exist.

        DatabaseException
            If sentiment data is unavailable.
        """

        logger.info(
            "Fetching latest sentiment | company=%s",
            company_name,
        )

        db = SessionLocal()

        try:

            company = self._get_company(
                db,
                company_name,
            )

            result = (
                db.query(
                    NewsMetadata,
                    SentimentScore,
                )
                .join(
                    SentimentScore,
                    NewsMetadata.id
                    == SentimentScore.news_id,
                )
                .filter(
                    SentimentScore.company_id
                    == company.id
                )
                .order_by(
                    NewsMetadata.published_date.desc()
                )
                .first()
            )

            if result is None:

                logger.warning(
                    "No sentiment found | company=%s",
                    company_name,
                )

                raise DatabaseException(
                    "No sentiment data available."
                )

            news, sentiment = result

            logger.info(
                "Latest sentiment retrieved | company=%s",
                company_name,
            )

            return {
                "title": news.title,
                "published_date": news.published_date,
                "sentiment": sentiment.sentiment_label,
                "confidence": round(
                    sentiment.confidence_score * 100,
                    2,
                ),
            }

        except (
            CompanyNotFoundException,
            DatabaseException,
            InvalidRequestException,
        ):
            raise

        except SQLAlchemyError as error:

            logger.exception(
                "Database error while retrieving sentiment."
            )

            db.rollback()

            raise DatabaseException(
                "Failed to retrieve sentiment."
            ) from error

        finally:

            db.close()

    # -----------------------------------------------------
    # Positive News
    # -----------------------------------------------------

    def get_positive_news(
        self,
        company_name: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Retrieve the latest positive news.

        Parameters
        ----------
        company_name : str
            Company name.

        limit : int
            Maximum number of articles.

        Returns
        -------
        list[dict[str, Any]]
            Positive news articles.
        """

        logger.info(
            "Fetching positive news | company=%s | limit=%s",
            company_name,
            limit,
        )

        if limit <= 0:

            raise InvalidRequestException(
                "Limit must be greater than zero."
            )

        limit = min(limit, 100)

        db = SessionLocal()

        try:

            company = self._get_company(
                db,
                company_name,
            )

            rows = (
                db.query(
                    NewsMetadata,
                    SentimentScore,
                )
                .join(
                    SentimentScore,
                    NewsMetadata.id
                    == SentimentScore.news_id,
                )
                .filter(
                    SentimentScore.company_id
                    == company.id
                )
                .filter(
                    SentimentScore.sentiment_label
                    == "positive"
                )
                .order_by(
                    NewsMetadata.published_date.desc()
                )
                .limit(limit)
                .all()
            )

            logger.info(
                "Retrieved %s positive news articles | company=%s",
                len(rows),
                company_name,
            )

            return [
                {
                    "title": news.title,
                    "source": news.source,
                    "published_date": news.published_date,
                    "confidence": round(
                        sentiment.confidence_score * 100,
                        2,
                    ),
                }
                for news, sentiment in rows
            ]

        except (
            CompanyNotFoundException,
            DatabaseException,
            InvalidRequestException,
        ):
            raise

        except SQLAlchemyError as error:

            logger.exception(
                "Database error while retrieving positive news."
            )

            db.rollback()

            raise DatabaseException(
                "Failed to retrieve positive news."
            ) from error

        finally:

            db.close()
    # -----------------------------------------------------
    # Negative News
    # -----------------------------------------------------

    def get_negative_news(
        self,
        company_name: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Retrieve the latest negative news.

        Parameters
        ----------
        company_name : str
            Company name.

        limit : int
            Maximum number of articles.

        Returns
        -------
        list[dict[str, Any]]
            Negative news articles.
        """

        logger.info(
            "Fetching negative news | company=%s | limit=%s",
            company_name,
            limit,
        )

        if limit <= 0:
            raise InvalidRequestException(
                "Limit must be greater than zero."
            )

        limit = min(limit, 100)

        db = SessionLocal()

        try:

            company = self._get_company(
                db,
                company_name,
            )

            rows = (
                db.query(
                    NewsMetadata,
                    SentimentScore,
                )
                .join(
                    SentimentScore,
                    NewsMetadata.id == SentimentScore.news_id,
                )
                .filter(
                    SentimentScore.company_id == company.id
                )
                .filter(
                    SentimentScore.sentiment_label == "negative"
                )
                .order_by(
                    NewsMetadata.published_date.desc()
                )
                .limit(limit)
                .all()
            )

            logger.info(
                "Retrieved %s negative news articles | company=%s",
                len(rows),
                company_name,
            )

            return [
                {
                    "title": news.title,
                    "source": news.source,
                    "published_date": news.published_date,
                    "confidence": round(
                        sentiment.confidence_score * 100,
                        2,
                    ),
                }
                for news, sentiment in rows
            ]

        except (
            CompanyNotFoundException,
            InvalidRequestException,
            DatabaseException,
        ):
            raise

        except SQLAlchemyError as error:

            logger.exception(
                "Database error while retrieving negative news."
            )

            db.rollback()

            raise DatabaseException(
                "Failed to retrieve negative news."
            ) from error

        finally:

            db.close()

    # -----------------------------------------------------
    # Search News
    # -----------------------------------------------------

    def search_news(
        self,
        company_name: str,
        keyword: str,
    ) -> list[dict[str, Any]]:
        """
        Search company news by keyword.

        Parameters
        ----------
        company_name : str
            Company name.

        keyword : str
            Search keyword.

        Returns
        -------
        list[dict[str, Any]]
            Matching news articles.
        """

        logger.info(
            "Searching news | company=%s | keyword=%s",
            company_name,
            keyword,
        )

        if not keyword.strip():
            raise InvalidRequestException(
                "Keyword cannot be empty."
            )

        db = SessionLocal()

        try:

            company = self._get_company(
                db,
                company_name,
            )

            rows = (
                db.query(
                    NewsMetadata,
                )
                .filter(
                    NewsMetadata.company_id == company.id
                )
                .filter(
                    NewsMetadata.title.ilike(
                        f"%{keyword}%"
                    )
                )
                .order_by(
                    NewsMetadata.published_date.desc()
                )
                .all()
            )

            logger.info(
                "Search returned %s news articles | company=%s",
                len(rows),
                company_name,
            )

            return [
                {
                    "title": row.title,
                    "source": row.source,
                    "published_date": row.published_date,
                    "url": row.url,
                }
                for row in rows
            ]

        except (
            CompanyNotFoundException,
            InvalidRequestException,
            DatabaseException,
        ):
            raise

        except SQLAlchemyError as error:

            logger.exception(
                "Database error while searching news."
            )

            db.rollback()

            raise DatabaseException(
                "Failed to search news."
            ) from error

        finally:

            db.close()
    # -----------------------------------------------------
    # News Summary
    # -----------------------------------------------------

    def get_news_summary(
        self,
        company_name: str,
    ) -> dict[str, Any]:
        """
        Retrieve an overall news summary
        for a company.

        Parameters
        ----------
        company_name : str
            Company name.

        Returns
        -------
        dict[str, Any]
            News summary including
            sentiment statistics.

        Raises
        ------
        CompanyNotFoundException
            If the company does not exist.

        DatabaseException
            If the database query fails.
        """

        logger.info(
            "Generating news summary | company=%s",
            company_name,
        )

        db = SessionLocal()

        try:

            company = self._get_company(
                db,
                company_name,
            )

            total_news = (
                db.query(NewsMetadata)
                .filter(
                    NewsMetadata.company_id == company.id
                )
                .count()
            )

            positive = (
                db.query(func.count(SentimentScore.id))
                .filter(
                    SentimentScore.company_id == company.id
                )
                .filter(
                    SentimentScore.sentiment_label == "positive"
                )
                .scalar()
                or 0
            )

            negative = (
                db.query(func.count(SentimentScore.id))
                .filter(
                    SentimentScore.company_id == company.id
                )
                .filter(
                    SentimentScore.sentiment_label == "negative"
                )
                .scalar()
                or 0
            )

            neutral = (
                db.query(func.count(SentimentScore.id))
                .filter(
                    SentimentScore.company_id == company.id
                )
                .filter(
                    SentimentScore.sentiment_label == "neutral"
                )
                .scalar()
                or 0
            )

            latest_news = (
                db.query(NewsMetadata)
                .filter(
                    NewsMetadata.company_id == company.id
                )
                .order_by(
                    NewsMetadata.published_date.desc()
                )
                .first()
            )

            if positive >= negative and positive >= neutral:
                overall_sentiment = "Positive"

            elif negative >= positive and negative >= neutral:
                overall_sentiment = "Negative"

            else:
                overall_sentiment = "Neutral"

            logger.info(
                "News summary generated | company=%s",
                company_name,
            )

            return {
                "company": company.company_name,
                "overall_sentiment": overall_sentiment,
                "total_news": total_news,
                "positive_news": positive,
                "negative_news": negative,
                "neutral_news": neutral,
                "latest_update": (
                    latest_news.published_date
                    if latest_news
                    else None
                ),
            }

        except (
            CompanyNotFoundException,
            InvalidRequestException,
            DatabaseException,
        ):
            raise

        except SQLAlchemyError as error:

            logger.exception(
                "Database error while generating news summary."
            )

            db.rollback()

            raise DatabaseException(
                "Failed to generate news summary."
            ) from error

        finally:

            db.close()


news_mcp = NewsMCP()
