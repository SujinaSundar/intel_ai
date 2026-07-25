"""
Vector Retrieval Service.

Provides a wrapper around the
vector retrieval engine.
"""

import logging

from app.exceptions.custom_exceptions import (
    InvalidRequestException,
)
from app.retrieval.retrieval_service import (
    retrieve_documents,
)

logger = logging.getLogger(__name__)


def vector_retrieve(
    query: str,
    company_name: str | None = None,
    top_k: int = 5,
) -> dict:
    """
    Retrieve documents using vector search.

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

    logger.info("Starting vector retrieval.")

    if not query.strip():
        logger.warning("Empty query received.")
        raise InvalidRequestException(
            "Query cannot be empty."
        )

    result = retrieve_documents(
        query=query,
        company_name=company_name,
        top_k=top_k,
    )

    logger.info(
        "Vector retrieval completed with %d documents.",
        len(result.get("documents", [])),
    )

    return result