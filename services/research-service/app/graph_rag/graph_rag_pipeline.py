"""
Graph RAG pipeline.
"""

import logging
import time

from app.exceptions.custom_exceptions import (
    InvalidRequestException,
)
from app.graph_rag.company_extractor import (
    extract_company,
)
from app.graph_rag.graph_context_builder import (
    build_graph_context,
)
from app.graph_rag.graph_prompt_template import (
    build_graph_prompt,
)
from app.llm.llm_service import (
    generate_answer,
)

logger = logging.getLogger(__name__)


def ask_graph_question(
    question: str,
    company_name: str | None = None,
) -> dict:
    """
    Execute the GraphRAG pipeline.

    Parameters
    ----------
    question : str
        User question.

    company_name : str | None
        Optional company filter.

    Returns
    -------
    dict
        GraphRAG response.
    """

    if not question or not question.strip():
        raise InvalidRequestException(
            "Question cannot be empty."
        )

    logger.info(
        "Executing GraphRAG pipeline."
    )

    # -----------------------------------
    # Extract company automatically
    # -----------------------------------

    if company_name is None:

        company_name = extract_company(
            question
        )

    if company_name is None:

        logger.warning(
            "No company detected in question."
        )

        return {
            "pipeline": "Graph RAG",
            "question": question,
            "company_name": None,
            "answer": "Company not found.",
            "documents": [],
            "metadata": [],
            "graph_context": [],
            "sentiment": None,
            "stock": None,
            "retrieval_time": 0.0,
            "num_chunks": 0,
        }

    logger.info(
        "Using company: %s",
        company_name,
    )

    # -----------------------------------
    # Graph Retrieval
    # -----------------------------------

    start_time = time.perf_counter()

    context = build_graph_context(
        question=question,
        company_name=company_name,
    )

    retrieval_time = (
        time.perf_counter() - start_time
    )

    logger.info(
        "Graph retrieval completed in %.3f seconds.",
        retrieval_time,
    )

    graph_documents = context[
        "graph_documents"
    ]

    logger.info(
        "Retrieved %d graph documents.",
        len(graph_documents),
    )

    # -----------------------------------
    # Prompt Construction
    # -----------------------------------

    prompt = build_graph_prompt(
        question=question,
        graph_documents=graph_documents,
    )

    logger.debug(
        "Graph prompt generated successfully."
    )

    # -----------------------------------
    # LLM Generation
    # -----------------------------------

    answer = generate_answer(
        prompt
    )

    logger.info(
        "GraphRAG answer generated successfully."
    )

    # -----------------------------------
    # Response
    # -----------------------------------

    return {
        "pipeline": "Graph RAG",
        "question": question,
        "company_name": company_name,
        "answer": answer,
        # Graph triples are returned as
        # documents for evaluation.
        "documents": graph_documents,
        "metadata": [],
        "graph_context": graph_documents,
        "sentiment": None,
        "stock": None,
        "retrieval_time": retrieval_time,
        "num_chunks": len(graph_documents),
    }