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
    SentimentScore
)


class NewsMCP:

    def __init__(self):

        self.db = SessionLocal()

    def __del__(self):

        self.db.close()

    # -----------------------------------------------------
    # Private Helper
    # -----------------------------------------------------

    def _get_company(
        self,
        company_name: str
    ):

        return (

            self.db.query(
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
        limit: int = 5
    ):

        company = self._get_company(company_name)

        if company is None:

            return {
                "error": "Company not found"
            }

        news = (

            self.db.query(
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

    # -----------------------------------------------------
    # Company News
    # -----------------------------------------------------

    def get_company_news(
        self,
        company_name: str
    ):

        return self.get_latest_news(
            company_name,
            limit=10
        )

    # -----------------------------------------------------
    # Latest Sentiment
    # -----------------------------------------------------

    def get_latest_sentiment(
        self,
        company_name: str
    ):

        company = self._get_company(company_name)

        if company is None:

            return {
                "error": "Company not found"
            }

        result = (

            self.db.query(
                NewsMetadata,
                SentimentScore
            )

            .join(
                SentimentScore,
                NewsMetadata.id == SentimentScore.news_id
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

            "confidence": sentiment.confidence_score

        }

    # -----------------------------------------------------
    # Positive News
    # -----------------------------------------------------

    def get_positive_news(
        self,
        company_name: str,
        limit: int = 5
    ):

        company = self._get_company(company_name)

        if company is None:

            return []

        rows = (

            self.db.query(
                NewsMetadata,
                SentimentScore
            )

            .join(
                SentimentScore,
                NewsMetadata.id == SentimentScore.news_id
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

                "confidence": sentiment.confidence_score

            }

            for news, sentiment in rows

        ]

    # -----------------------------------------------------
    # Negative News
    # -----------------------------------------------------

    def get_negative_news(
        self,
        company_name: str,
        limit: int = 5
    ):

        company = self._get_company(company_name)

        if company is None:

            return []

        rows = (

            self.db.query(
                NewsMetadata,
                SentimentScore
            )

            .join(
                SentimentScore,
                NewsMetadata.id == SentimentScore.news_id
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

                "confidence": sentiment.confidence_score

            }

            for news, sentiment in rows

        ]

    # -----------------------------------------------------
    # Search News
    # -----------------------------------------------------

    def search_news(
        self,
        company_name: str,
        keyword: str
    ):

        company = self._get_company(company_name)

        if company is None:

            return []

        rows = (

            self.db.query(
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

    # -----------------------------------------------------
    # News Summary
    # -----------------------------------------------------

    def get_news_summary(
        self,
        company_name: str
    ):

        company = self._get_company(company_name)

        if company is None:

            return {
                "error": "Company not found"
            }

        total_news = (

            self.db.query(
                NewsMetadata
            )

            .filter(
                NewsMetadata.company_id == company.id
            )

            .count()

        )

        positive = (

            self.db.query(
                func.count(SentimentScore.id)
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

            self.db.query(
                func.count(SentimentScore.id)
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

            self.db.query(
                func.count(SentimentScore.id)
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

            self.db.query(
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