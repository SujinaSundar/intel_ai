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

import logging

from app.exceptions.custom_exceptions import (
    InvalidRequestException,
)
from app.graph_rag.graph_retriever import (
    retrieve_graph_context,
)

logger = logging.getLogger(__name__)


def build_graph_context(
    question: str,
    company_name: str,
) -> dict:
    """
    Build graph context using GraphRAG.

    Parameters
    ----------
    question : str
        User question.

    company_name : str
        Company extracted from the question.

    Returns
    -------
    dict
        Graph retrieval context.
    """

    logger.info(
        "Building GraphRAG context for company: %s",
        company_name,
    )

    if not question.strip():
        raise InvalidRequestException(
            "Question cannot be empty."
        )

    if not company_name.strip():
        raise InvalidRequestException(
            "Company name cannot be empty."
        )

    graph_documents = retrieve_graph_context(
        company_name=company_name,
        question=question,
        limit=20,
    )

    logger.info(
        "Retrieved %d graph relationships.",
        len(graph_documents),
    )

    return {
        "graph_documents": graph_documents,
    }