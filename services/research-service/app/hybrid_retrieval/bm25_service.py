"""
BM25 Retrieval Service.

Workflow
--------
Question
    ↓
Tokenize Query
    ↓
BM25 Search
    ↓
Top K Chunks
"""

import logging

from rank_bm25 import BM25Okapi
from sqlalchemy.exc import SQLAlchemyError

from app.database.connection import SessionLocal
from app.database.models import (
    Company,
    DocumentChunk,
    ResearchReport,
)
from app.exceptions.custom_exceptions import (
    DatabaseException,
    InvalidRequestException,
)

logger = logging.getLogger(__name__)


def bm25_retrieve(
    query: str,
    company_name: str | None = None,
    top_k: int = 5,
) -> dict:
    """
    Retrieve relevant chunks using BM25.

    Parameters
    ----------
    query : str
        User query.

    company_name : str | None
        Optional company filter.

    top_k : int
        Number of documents to retrieve.

    Returns
    -------
    dict
        Retrieved documents and metadata.
    """

    if not query.strip():
        raise InvalidRequestException(
            "Query cannot be empty."
        )

    logger.info("Starting BM25 retrieval.")

    db = SessionLocal()

    try:

        rows = (
            db.query(
                DocumentChunk,
                ResearchReport,
                Company,
            )
            .join(
                ResearchReport,
                DocumentChunk.report_id == ResearchReport.id,
            )
            .join(
                Company,
                ResearchReport.company_id == Company.id,
            )
        )

        # -------------------------------------------------
        # Optional Company Filter
        # -------------------------------------------------

        if company_name:

            logger.info(
                "Filtering BM25 documents for company: %s",
                company_name,
            )

            rows = rows.filter(
                Company.company_name.ilike(
                    f"%{company_name}%"
                )
            )

        rows = rows.all()

        if not rows:

            logger.info(
                "No BM25 documents found."
            )

            return {
                "documents": [],
                "metadata": [],
            }

        documents = [
            chunk.chunk_text
            for chunk, _, _ in rows
        ]

        tokenized_corpus = [
            document.lower().split()
            for document in documents
        ]

        bm25 = BM25Okapi(
            tokenized_corpus
        )

        tokenized_query = (
            query.lower().split()
        )

        scores = bm25.get_scores(
            tokenized_query
        )

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True,
        )[:top_k]

        retrieved_documents = []
        metadata = []

        for index in ranked_indices:

            chunk, report, company = rows[index]

            retrieved_documents.append(
                chunk.chunk_text
            )

            metadata.append(
                {
                    "document": chunk.chunk_text,
                    "company_id": company.id,
                    "company_name": company.company_name,
                    "report_id": report.id,
                    "report_type": report.report_type,
                    "year": report.year,
                    "chunk_number": chunk.chunk_number,
                }
            )

        logger.info(
            "BM25 retrieval completed with %d documents.",
            len(retrieved_documents),
        )

        return {
            "documents": retrieved_documents,
            "metadata": metadata,
        }

    except SQLAlchemyError as error:

        logger.exception(
            "BM25 database operation failed."
        )

        raise DatabaseException(
            str(error)
        ) from error

    finally:

        db.close()

        logger.info(
            "Database session closed."
        )