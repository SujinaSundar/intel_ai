"""
News MCP

Provides news retrieval tools
for the Trading Research Agent.
"""

from sqlalchemy import func

from app.database.connection import SessionLocal
from app.database.models import (
    Company,
    NewsMetadata,
    SentimentScore,
)


class NewsMCP:
    """
    News MCP.

    Provides news retrieval
    tools for company news
    and sentiment analysis.
    """

    # -----------------------------------------------------
    # Private Helper
    # -----------------------------------------------------

    def _get_company(
        self,
        db,
        company_name: str,
    ):

        return (

            db.query(
                Company
            )

            .filter(
                Company.company_name == company_name
            )

            .first()

        )

    # -----------------------------------------------------
    # Latest News
    # -----------------------------------------------------

    def get_latest_news(
        self,
        company_name: str,
        limit: int = 5,
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

            news = (

                db.query(
                    NewsMetadata
                )

                .filter(
                    NewsMetadata.company_id == company.id
                )

                .order_by(
                    NewsMetadata.published_date.desc()
                )

                .limit(limit)

                .all()

            )

            return [

                {

                    "title": row.title,

                    "source": row.source,

                    "published_date": row.published_date,

                    "url": row.url

                }

                for row in news

            ]

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()

    # -----------------------------------------------------
    # Company News
    # -----------------------------------------------------

    def get_company_news(
        self,
        company_name: str,
    ):

        return self.get_latest_news(
            company_name,
            limit=10,
        )
    # -----------------------------------------------------
    # Latest Sentiment
    # -----------------------------------------------------

    def get_latest_sentiment(
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

            result = (

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

                .order_by(
                    NewsMetadata.published_date.desc()
                )

                .first()

            )

            if result is None:

                return {
                    "error": "No sentiment found"
                }

            news, sentiment = result

            return {

                "title": news.title,

                "published_date": news.published_date,

                "sentiment": sentiment.sentiment_label,

                "confidence": sentiment.confidence_score,

            }

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()

    # -----------------------------------------------------
    # Positive News
    # -----------------------------------------------------

    def get_positive_news(
        self,
        company_name: str,
        limit: int = 5,
    ):

        db = SessionLocal()

        try:

            company = self._get_company(
                db,
                company_name,
            )

            if company is None:

                return []

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
                    SentimentScore.sentiment_label == "positive"
                )

                .order_by(
                    NewsMetadata.published_date.desc()
                )

                .limit(limit)

                .all()

            )

            return [

                {

                    "title": news.title,

                    "source": news.source,

                    "published_date": news.published_date,

                    "confidence": sentiment.confidence_score,

                }

                for news, sentiment in rows

            ]

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()

    # -----------------------------------------------------
    # Negative News
    # -----------------------------------------------------

    def get_negative_news(
        self,
        company_name: str,
        limit: int = 5,
    ):

        db = SessionLocal()

        try:

            company = self._get_company(
                db,
                company_name,
            )

            if company is None:

                return []

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

            return [

                {

                    "title": news.title,

                    "source": news.source,

                    "published_date": news.published_date,

                    "confidence": sentiment.confidence_score,

                }

                for news, sentiment in rows

            ]

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()
    # -----------------------------------------------------
    # Search News
    # -----------------------------------------------------

    def search_news(
        self,
        company_name: str,
        keyword: str,
    ):

        db = SessionLocal()

        try:

            company = self._get_company(
                db,
                company_name,
            )

            if company is None:

                return []

            rows = (

                db.query(
                    NewsMetadata
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

            return [

                {

                    "title": row.title,

                    "source": row.source,

                    "published_date": row.published_date,

                    "url": row.url

                }

                for row in rows

            ]

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()

    # -----------------------------------------------------
    # News Summary
    # -----------------------------------------------------

    def get_news_summary(
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

            total_news = (

                db.query(
                    NewsMetadata
                )

                .filter(
                    NewsMetadata.company_id == company.id
                )

                .count()

            )

            positive = (

                db.query(
                    func.count(
                        SentimentScore.id
                    )
                )

                .filter(
                    SentimentScore.company_id == company.id
                )

                .filter(
                    SentimentScore.sentiment_label == "positive"
                )

                .scalar()

            )

            negative = (

                db.query(
                    func.count(
                        SentimentScore.id
                    )
                )

                .filter(
                    SentimentScore.company_id == company.id
                )

                .filter(
                    SentimentScore.sentiment_label == "negative"
                )

                .scalar()

            )

            neutral = (

                db.query(
                    func.count(
                        SentimentScore.id
                    )
                )

                .filter(
                    SentimentScore.company_id == company.id
                )

                .filter(
                    SentimentScore.sentiment_label == "neutral"
                )

                .scalar()

            )

            latest_news = (

                db.query(
                    NewsMetadata
                )

                .filter(
                    NewsMetadata.company_id == company.id
                )

                .order_by(
                    NewsMetadata.published_date.desc()
                )

                .first()

            )

            return {

                "company": company.company_name,

                "total_news": total_news,

                "positive_news": positive,

                "negative_news": negative,

                "neutral_news": neutral,

                "latest_update": (

                    latest_news.published_date

                    if latest_news

                    else None

                )

            }

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()