"""
Research Routes.

Exposes REST APIs for
Hybrid GraphRAG retrieval.
"""

from fastapi import (
    APIRouter,
    HTTPException
)

from app.schemas.research import (
    ResearchRequest
)

from app.hybrid_graph_rag.hybrid_graph_pipeline import (
    ask_hybrid_graph_question
)


router = APIRouter(

    prefix="/research",

    tags=["Research"]

)


@router.post("/ask")
def ask_research(
    request: ResearchRequest
):
    """
    Answer a research question.

    Parameters
    ----------
    request : ResearchRequest

    Returns
    -------
    dict
        Hybrid GraphRAG response.
    """

    try:

        return ask_hybrid_graph_question(

            question=request.question

        )

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=str(error)

        )


@router.get("/health")
def health_check():
    """
    Research service health check.

    Returns
    -------
    dict
    """

    return {

        "service": "Research Service",

        "status": "Running"

    }