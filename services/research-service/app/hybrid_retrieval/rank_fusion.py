"""
Reciprocal Rank Fusion.

Combines Vector Search and BM25
results using the Reciprocal Rank
Fusion (RRF) algorithm.
"""

import logging

from app.exceptions.custom_exceptions import (
    InvalidRequestException,
)

logger = logging.getLogger(__name__)


def reciprocal_rank_fusion(
    vector_results: list[str],
    bm25_results: list[str],
    k: int = 60,
) -> list[str]:
    """
    Combine Vector Search and BM25
    results using Reciprocal Rank Fusion.

    Parameters
    ----------
    vector_results : list[str]
        Ranked vector search results.

    bm25_results : list[str]
        Ranked BM25 search results.

    k : int
        RRF constant.

    Returns
    -------
    list[str]
        Fused ranking of unique documents.
    """

    logger.info("Starting Reciprocal Rank Fusion.")

    if k <= 0:
        raise InvalidRequestException(
            "RRF constant 'k' must be greater than zero."
        )

    scores: dict[str, float] = {}

    # -------------------------------------------------
    # Vector Search Ranking
    # -------------------------------------------------

    for rank, document in enumerate(
        vector_results,
        start=1,
    ):

        scores[document] = (
            scores.get(document, 0.0)
            + 1 / (k + rank)
        )

    # -------------------------------------------------
    # BM25 Ranking
    # -------------------------------------------------

    for rank, document in enumerate(
        bm25_results,
        start=1,
    ):

        scores[document] = (
            scores.get(document, 0.0)
            + 1 / (k + rank)
        )

    ranked_documents = sorted(
        scores,
        key=scores.get,
        reverse=True,
    )

    logger.info(
        "Reciprocal Rank Fusion completed with %d documents.",
        len(ranked_documents),
    )

    return ranked_documents