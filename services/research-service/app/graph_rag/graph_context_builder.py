"""
Graph Context Builder.

Workflow
--------
Question
    ↓
Graph Retrieval
    ↓
Graph Context
"""

from app.graph_rag.graph_retriever import (
    retrieve_graph_context
)


def build_graph_context(
    question: str,
    company_name: str
) -> dict:
    """
    Build graph context.

    Parameters
    ----------
    question : str

    company_name : str

    Returns
    -------
    dict
    """

    graph_documents = retrieve_graph_context(

        company_name=company_name,

        question=question,

        limit=20

    )

    return {

        "graph_documents": graph_documents

    }