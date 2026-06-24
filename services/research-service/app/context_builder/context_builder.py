"""
Context builder.

Workflow
--------
Question
    ↓
Report Retrieval
    ↓
Sentiment Retrieval
    ↓
Stock Price Retrieval
    ↓
Combined Context
"""

from app.database.connection import (
    SessionLocal
)

from app.database.models import (
    Company,
    StockPrice,
    SentimentScore
)

from app.retrieval.retrieval_service import (
    retrieve_documents
)


def build_context(
    question: str,
    company_name: str
) -> dict:
    """
    Build context for RAG.

    Parameters
    ----------
    question : str

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

        documents = retrieve_documents(
            query=question,
            top_k=5
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

        return {

            "documents": documents,

            "sentiment": sentiment,

            "stock": stock
        }

    finally:

        db.close()