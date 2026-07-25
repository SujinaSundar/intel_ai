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

import logging

from sqlalchemy.exc import SQLAlchemyError

from app.database.connection import SessionLocal
from app.database.models import (
    Company,
    SentimentScore,
    StockPrice,
)
from app.exceptions.custom_exceptions import (
    CompanyNotFoundException,
    DatabaseException,
    InvalidRequestException,
)
from app.graph_rag.graph_retriever import (
    retrieve_graph_context,
)

logger = logging.getLogger(__name__)


def build_graph_context(
    company_name: str,
) -> dict:
    """
    Build graph context for a company.

    Parameters
    ----------
    company_name : str
        Company name.

    Returns
    -------
    dict
        Graph context, sentiment, and stock data.
    """

    if not company_name or not company_name.strip():
        raise InvalidRequestException(
            "Company name cannot be empty."
        )

    db = SessionLocal()

    try:

        logger.info(
            "Building graph context for company: %s",
            company_name,
        )

        company = (
            db.query(
                Company
            )
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

        graph_documents = retrieve_graph_context(
            company.company_name
        )

        logger.info(
            "Retrieved %d graph documents.",
            len(graph_documents),
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

        logger.info(
            "Graph context built successfully."
        )

        return {
            "graph_documents": graph_documents,
            "sentiment": sentiment_text,
            "stock": stock_text,
        }

    except SQLAlchemyError as error:

        logger.exception(
            "Database error while building graph context."
        )

        raise DatabaseException(
            f"Failed to build graph context: {error}"
        ) from error

    finally:

        db.close()

        logger.info(
            "Database session closed."
        )