"""
Hybrid Graph Context Builder.

Combines Hybrid RAG retrieval
and GraphRAG retrieval.
"""

import logging

from app.context_builder.hybrid_context_builder import (
    build_hybrid_context,
)
from app.graph_rag.graph_context_builder import (
    build_graph_context,
)

logger = logging.getLogger(__name__)


def build_hybrid_graph_context(
    question: str,
    company_name: str,
) -> dict:
    """
    Build the Hybrid GraphRAG context.

    Parameters
    ----------
    question : str
        User question.

    company_name : str
        Company extracted from the question.

    Returns
    -------
    dict
        Combined Hybrid RAG and GraphRAG context.
    """

    logger.info(
        "Building Hybrid RAG context for company: %s",
        company_name,
    )

    # -------------------------------------------------
    # Hybrid RAG Context
    # -------------------------------------------------

    hybrid_context = build_hybrid_context(
        question=question,
        company_name=company_name,
    )

    logger.info(
        "Hybrid RAG context built successfully."
    )

    # -------------------------------------------------
    # GraphRAG Context
    # -------------------------------------------------

    logger.info(
        "Building GraphRAG context."
    )

    graph_context = build_graph_context(
        question=question,
        company_name=company_name,
    )

    logger.info(
        "GraphRAG context built successfully."
    )

    # -------------------------------------------------
    # Combined Context
    # -------------------------------------------------

    combined_context = {
        "documents": hybrid_context["documents"],
        "metadata": hybrid_context["metadata"],
        "sentiment": hybrid_context["sentiment"],
        "stock": hybrid_context["stock"],
        "graph_documents": graph_context["graph_documents"],
    }

    logger.info(
        "Hybrid GraphRAG context built successfully."
    )

    return combined_context