"""
Vector retrieval service.
"""

from app.retrieval.retrieval_service import (
    retrieve_documents
)


def vector_retrieve(
    query: str,
    top_k: int = 5
) -> list[str]:
    """
    Retrieve documents using vector search.

    Parameters
    ----------
    query : str

    top_k : int

    Returns
    -------
    list[str]
    """

    return retrieve_documents(
        query=query,
        top_k=top_k
    )