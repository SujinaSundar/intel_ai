"""
Vector retrieval service.
"""

from app.retrieval.retrieval_service import (
    retrieve_documents
)


def vector_retrieve(
    query: str,
    company_name: str | None = None,
    top_k: int = 5
) -> dict:
    """
    Retrieve documents using vector search.

    Parameters
    ----------
    query : str

    company_name : str | None
        Optional company filter.

    top_k : int

    Returns
    -------
    dict
    """

    return retrieve_documents(

        query=query,

        company_name=company_name,

        top_k=top_k

    )