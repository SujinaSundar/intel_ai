"""
Research Routes.

Exposes REST APIs for
Hybrid GraphRAG retrieval.
"""

import logging

from fastapi import APIRouter

from app.hybrid_graph_rag.hybrid_graph_pipeline import (
    ask_hybrid_graph_question,
)
from app.schemas.research import (
    ResearchRequest,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/research",
    tags=["Research"],
)


# ---------------------------------------------------------
# Ask Research Question
# ---------------------------------------------------------

@router.post("/ask")
def ask_research(
    request: ResearchRequest,
) -> dict:
    """
    Answer a research question using
    the Hybrid GraphRAG pipeline.

    Parameters
    ----------
    request : ResearchRequest
        User research request.

    Returns
    -------
    dict
        Hybrid GraphRAG response.
    """

    logger.info(
        "Processing research request."
    )

    response = ask_hybrid_graph_question(
        question=request.question,
    )

    logger.info(
        "Research request completed successfully."
    )

    return response


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@router.get("/health")
def health_check() -> dict[str, str]:
    """
    Research Service health check.

    Returns
    -------
    dict[str, str]
        Service status.
    """

    logger.info(
        "Health check endpoint accessed."
    )

    return {
        "service": "Research Service",
        "status": "Running",
    }