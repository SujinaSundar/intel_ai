"""
Hybrid Retrieval Service.

Combines Vector Search and BM25
using Reciprocal Rank Fusion (RRF).
"""

import logging

from app.exceptions.custom_exceptions import (
    InvalidRequestException,
)
from app.hybrid_retrieval.bm25_service import (
    bm25_retrieve,
)
from app.hybrid_retrieval.rank_fusion import (
    reciprocal_rank_fusion,
)
from app.hybrid_retrieval.vector_service import (
    vector_retrieve,
)

logger = logging.getLogger(__name__)


def hybrid_retrieve(
    query: str,
    company_name: str | None = None,
    top_k: int = 5,
) -> dict:
    """
    Perform Hybrid Retrieval using
    Vector Search and BM25.

    Parameters
    ----------
    query : str
        User query.

    company_name : str | None
        Optional company filter.

    top_k : int
        Number of documents to return.

    Returns
    -------
    dict
        Hybrid retrieval results.
    """

    logger.info("Starting Hybrid Retrieval.")

    if not query.strip():
        logger.warning("Received empty query.")
        raise InvalidRequestException(
            "Query cannot be empty."
        )

    logger.info("Running Vector Retrieval.")

    vector_results = vector_retrieve(
        query=query,
        company_name=company_name,
        top_k=top_k,
    )

    logger.info(
        "Vector Retrieval returned %d documents.",
        len(vector_results["documents"]),
    )

    logger.info("Running BM25 Retrieval.")

    bm25_results = bm25_retrieve(
        query=query,
        company_name=company_name,
        top_k=top_k,
    )

    logger.info(
        "BM25 Retrieval returned %d documents.",
        len(bm25_results["documents"]),
    )

    logger.info("Performing Reciprocal Rank Fusion.")

    fused_documents = reciprocal_rank_fusion(
        vector_results["documents"],
        bm25_results["documents"],
    )

    logger.info(
        "Hybrid Retrieval completed with %d fused documents.",
        len(fused_documents),
    )

    return {
        "documents": fused_documents[:top_k],

        # TODO:
        # Metadata fusion will be added later.
        "metadata": [],
    }