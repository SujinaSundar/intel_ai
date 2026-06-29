"""
Hybrid retrieval service.
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
    company_name: str | None = None,
    top_k: int = 5
) -> dict:
    """
    Hybrid retrieval.
    """

    vector_results = vector_retrieve(
        query=query,
        company_name=company_name,
        top_k=top_k
    )

    bm25_results = bm25_retrieve(
        query=query,
        company_name=company_name,
        top_k=top_k
    )

    fused_documents = reciprocal_rank_fusion(
        vector_results["documents"],
        bm25_results["documents"]
    )

    return {

        "documents": fused_documents[:top_k],

        # Metadata fusion will be added later
        "metadata": []

    }