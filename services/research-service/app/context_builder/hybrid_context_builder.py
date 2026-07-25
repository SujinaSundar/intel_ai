"""
Hybrid context builder.

Workflow
--------
Question
    ↓
Hybrid Retrieval
(Vector + BM25)
    ↓
Sentiment Retrieval (Optional)
    ↓
Stock Retrieval (Optional)
    ↓
Combined Context
"""

import logging

from app.database.connection import SessionLocal
from app.database.models import (
    Company,
    SentimentScore,
    StockPrice,
)
from app.exceptions.custom_exceptions import (
    CompanyNotFoundException,
    DatabaseException,
)
from app.hybrid_retrieval.hybrid_service import (
    hybrid_retrieve,
)
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


def build_hybrid_context(
    question: str,
    company_name: str | None = None,
) -> dict:
    """
    Build context using Hybrid RAG.

    Parameters
    ----------
    question : str
        User question.

    company_name : str | None
        Optional company filter.

    Returns
    -------
    dict
        Hybrid retrieval context.
    """

    logger.info("Building Hybrid RAG context.")

    db = SessionLocal()

    try:

        sentiment = None
        stock = None
        metadata = []

        # -------------------------------------------------
        # Company-specific Retrieval
        # -------------------------------------------------

        if company_name:

            logger.info(
                "Searching company: %s",
                company_name,
            )

            company = (
                db.query(Company)
                .filter(
                    Company.company_name.ilike(
                        f"%{company_name}%"
                    )
                )
                .first()
            )

            if company is None:

                logger.warning(
                    "Company not found: %s",
                    company_name,
                )

                raise CompanyNotFoundException(
                    company_name
                )

            logger.info(
                "Running Hybrid Retrieval."
            )

            retrieval_result = hybrid_retrieve(
                query=question,
                company_name=company_name,
                top_k=5,
            )

            documents = retrieval_result["documents"]
            metadata = retrieval_result["metadata"]

            logger.info(
                "Fetching latest sentiment."
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

            logger.info(
                "Fetching latest stock data."
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

        # -------------------------------------------------
        # Global Retrieval
        # -------------------------------------------------

        else:

            logger.info(
                "Running global Hybrid Retrieval."
            )

            retrieval_result = hybrid_retrieve(
                query=question,
                company_name=None,
                top_k=5,
            )

            documents = retrieval_result["documents"]
            metadata = retrieval_result["metadata"]

        logger.info(
            "Hybrid context built successfully."
        )

        return {
        "documents": documents,
        "metadata": metadata,
        "sentiment": (
            {
                "sentiment_label": sentiment.sentiment_label,
                "confidence_score": sentiment.confidence_score,
                "created_at": sentiment.created_at,
            }
            if sentiment
            else None
        ),
        "stock": (
            {
                "trade_date": stock.trade_date,
                "open_price": stock.open_price,
                "high_price": stock.high_price,
                "low_price": stock.low_price,
                "close_price": stock.close_price,
                "volume": stock.volume,
            }
            if stock
            else None
        ),
    }

    except SQLAlchemyError as error:

        logger.exception(
            "Database operation failed."
        )

        raise DatabaseException(
            str(error)
        ) from error

    finally:

        db.close()

        logger.info(
            "Database session closed."
        )