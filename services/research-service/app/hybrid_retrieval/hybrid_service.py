"""
Hybrid retrieval service.

Workflow
--------
Question
    ↓
Vector Search
    +
BM25 Search
    ↓
Reciprocal Rank Fusion
    ↓
Top K Documents
"""

from app.hybrid_retrieval.vector_service import (
    vector_retrieve
)

from app.hybrid_retrieval.bm25_service import (
    bm25_retrieve
)

from app.hybrid_retrieval.rank_fusion import (
    reciprocal_rank_fusion
)


def hybrid_retrieve(
    query: str,
    top_k: int = 5
) -> list[str]:
    """
    Hybrid retrieval.

    Parameters
    ----------
    query : str

    top_k : int

    Returns
    -------
    list[str]
    """

    vector_results = vector_retrieve(
        query=query,
        top_k=top_k
    )

    bm25_results = bm25_retrieve(
        query=query,
        top_k=top_k
    )

    fused_results = reciprocal_rank_fusion(
        vector_results,
        bm25_results
    )

    return fused_results[:top_k]