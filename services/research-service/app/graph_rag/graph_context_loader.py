"""
Graph context builder.

Workflow
--------
Question
    ↓
Graph Retrieval
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

from app.graph_rag.graph_retriever import (
    retrieve_graph_context
)


def build_graph_context(
    company_name: str
) -> dict:
    """
    Build graph context.

    Parameters
    ----------
    company_name : str

    Returns
    -------
    dict
    """

    db = SessionLocal()

    try:

        company = (
            db.query(
                Company
            )
            .filter(
                Company.company_name.ilike(
                    company_name
                )
            )
            .first()
        )

        if company is None:

            return {}

        graph_documents = retrieve_graph_context(
            company_name
        )

        sentiment = (
            db.query(
                SentimentScore
            )
            .filter(
                SentimentScore.company_id == company.id
            )
            .order_by(
                SentimentScore.created_at.desc()
            )
            .first()
        )

        stock = (
            db.query(
                StockPrice
            )
            .filter(
                StockPrice.company_id == company.id
            )
            .order_by(
                StockPrice.trade_date.desc()
            )
            .first()
        )

        sentiment_text = "No sentiment available."

        if sentiment:

            sentiment_text = (
                f"Label: {sentiment.sentiment_label}\n"
                f"Confidence: {sentiment.confidence_score}"
            )

        stock_text = "No stock data available."

        if stock:

            stock_text = (
                f"Trade Date: {stock.trade_date}\n"
                f"Close Price: {stock.close_price}\n"
                f"Volume: {stock.volume}"
            )

        return {

            "graph_documents": graph_documents,

            "sentiment": sentiment_text,

            "stock": stock_text
        }

    finally:

        db.close()