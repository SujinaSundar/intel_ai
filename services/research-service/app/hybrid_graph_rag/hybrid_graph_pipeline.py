"""
Hybrid GraphRAG Pipeline.
"""

import logging
import time

from app.exceptions.custom_exceptions import (
    InvalidRequestException,
)
from app.graph_rag.company_extractor import (
    extract_company,
)
from app.hybrid_graph_rag.hybrid_graph_context_builder import (
    build_hybrid_graph_context,
)
from app.hybrid_graph_rag.hybrid_graph_prompt import (
    build_hybrid_graph_prompt,
)
from app.llm.llm_service import (
    generate_answer,
)

logger = logging.getLogger(__name__)


def needs_market_context(
    question: str,
) -> bool:
    """
    Determine whether market data should
    be included in the Hybrid GraphRAG context.

    Parameters
    ----------
    question : str
        User question.

    Returns
    -------
    bool
        True if market data should be included.
    """

    keywords = {
        "invest",
        "investment",
        "stock",
        "share",
        "price",
        "market",
        "buy",
        "sell",
        "trading",
        "target",
        "valuation",
        "returns",
        "performance",
    }

    question = question.lower()

    return any(
        keyword in question
        for keyword in keywords
    )


def ask_hybrid_graph_question(
    question: str,
) -> dict:
    """
    Execute the Hybrid GraphRAG pipeline.

    Parameters
    ----------
    question : str
        User research question.

    Returns
    -------
    dict
        Hybrid GraphRAG response.
    """

    logger.info("Starting Hybrid GraphRAG pipeline.")
    logger.info("Question: %s", question)

    # -------------------------------------------------
    # Company Extraction
    # -------------------------------------------------

    company_name = extract_company(question)

    if company_name is None:
        logger.warning(
            "Unable to identify company from question."
        )
        raise InvalidRequestException(
            "Unable to identify a company from the question."
        )

    logger.info(
        "Detected company: %s",
        company_name,
    )

    # -------------------------------------------------
    # Hybrid Graph Retrieval
    # -------------------------------------------------

    logger.info("Building Hybrid Graph context.")

    start_time = time.perf_counter()

    context = build_hybrid_graph_context(
        question=question,
        company_name=company_name,
    )

    retrieval_time = (
        time.perf_counter() - start_time
    )

    logger.info(
        "Context built successfully in %.3f seconds.",
        retrieval_time,
    )

    # -------------------------------------------------
    # Optional Market Context
    # -------------------------------------------------

    if needs_market_context(question):

        sentiment_text = (
            str(context["sentiment"])
            if context["sentiment"]
            else "No sentiment found."
        )

        stock_text = (
            str(context["stock"])
            if context["stock"]
            else "No stock data found."
        )

    else:

        sentiment_text = ""
        stock_text = ""

    # -------------------------------------------------
    # Prompt Construction
    # -------------------------------------------------

    logger.info("Building LLM prompt.")

    prompt = build_hybrid_graph_prompt(
        question=question,
        documents=context["documents"],
        graph_documents=context["graph_documents"],
        sentiment_text=sentiment_text,
        stock_text=stock_text,
    )

    # -------------------------------------------------
    # LLM Generation
    # -------------------------------------------------

    logger.info("Generating response from LLM.")

    answer = generate_answer(prompt)

    logger.info("Hybrid GraphRAG completed successfully.")

    # -------------------------------------------------
    # Response
    # -------------------------------------------------

    return {
        "pipeline": "Hybrid GraphRAG",
        "question": question,
        "company_name": company_name,
        "answer": answer,
        "documents": context["documents"],
        "metadata": context["metadata"],
        "graph_context": context["graph_documents"],
        "sentiment": context["sentiment"],
        "stock": context["stock"],
        "retrieval_time": retrieval_time,
        "num_chunks": len(
            context["documents"]
        ),
        "num_triples": len(
            context["graph_documents"]
        ),
    }