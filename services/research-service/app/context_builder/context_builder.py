"""
Context builder.

Workflow
--------
Question
    ↓
Report Retrieval
    ↓
Sentiment Retrieval (Optional)
    ↓
Stock Price Retrieval (Optional)
    ↓
Combined Context
"""

from app.database.connection import SessionLocal

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
    company_name: str | None = None
) -> dict:
    """
    Build context for RAG.

    Parameters
    ----------
    question : str

    company_name : str | None
        Optional company filter.

    Returns
    -------
    dict
    """

    db = SessionLocal()

    try:

        company = None

        sentiment = None

        stock = None

        metadata = []

        # -----------------------------
        # Company-specific retrieval
        # -----------------------------

        if company_name:

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

                return {

                    "documents": [],

                    "metadata": [],

                    "sentiment": None,

                    "stock": None
                }

            retrieval_result = retrieve_documents(

                query=question,

                company_name=company_name,

                top_k=5

            )

            documents = retrieval_result["documents"]

            metadata = retrieval_result["metadata"]

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

        # -----------------------------
        # Global retrieval
        # -----------------------------

        else:

            retrieval_result = retrieve_documents(

                query=question,

                company_name=None,

                top_k=5

            )

            documents = retrieval_result["documents"]

            metadata = retrieval_result["metadata"]

        return {

            "documents": documents,

            "metadata": metadata,

            "sentiment": sentiment,

            "stock": stock
        }

    finally:

        db.close()