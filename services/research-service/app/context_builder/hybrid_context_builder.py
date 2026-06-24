"""
Hybrid context builder.

Workflow
--------
Question
    ↓
Hybrid Retrieval
(Vector + BM25)
    ↓
Sentiment
    ↓
Stock Data
    ↓
Combined Context
"""

from app.database.connection import SessionLocal

from app.database.models import (
    Company,
    SentimentScore,
    StockPrice
)

from app.hybrid_retrieval.hybrid_service import (
    hybrid_retrieve
)


def build_hybrid_context(
    question: str,
    company_name: str
) -> dict:
    """
    Build context using hybrid retrieval.

    Parameters
    ----------
    question : str
        User question.

    company_name : str
        Company name.

    Returns
    -------
    dict
    """

    db = SessionLocal()

    try:

        company = (
            db.query(Company)
            .filter(
                Company.company_name == company_name
            )
            .first()
        )

        if company is None:

            raise ValueError(
                "Company not found."
            )

        documents = hybrid_retrieve(
            query=question,
            top_k=5
        )

        sentiment = (
            db.query(SentimentScore)
            .filter(
                SentimentScore.company_id == company.id
            )
            .order_by(
                SentimentScore.created_at.desc()
            )
            .first()
        )

        stock = (
            db.query(StockPrice)
            .filter(
                StockPrice.company_id == company.id
            )
            .order_by(
                StockPrice.trade_date.desc()
            )
            .first()
        )
        sentiment_text = "No sentiment data available."

        if sentiment:

            sentiment_text = (
                f"Label: {sentiment.sentiment_label}\n"
                f"Confidence: {sentiment.confidence_score}"
            )

        stock_text = "No stock data available."

        if stock:

            stock_text = (
                f"Trade Date: {stock.trade_date}\n"
                f"Open Price: {stock.open_price}\n"
                f"High Price: {stock.high_price}\n"
                f"Low Price: {stock.low_price}\n"
                f"Close Price: {stock.close_price}\n"
                f"Volume: {stock.volume}"
            )

        return {

            "documents": documents,

            "sentiment": sentiment_text,

            "stock": stock_text
        }

    finally:

        db.close()