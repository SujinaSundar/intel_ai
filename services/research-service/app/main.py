"""
Research Service.

Exposes APIs for
Hybrid GraphRAG retrieval.
"""

from fastapi import FastAPI

from app.routes.research import (
    router as research_router
)

app = FastAPI(
    title="Research Service",
    description=(
        "Provides research retrieval "
        "using Hybrid GraphRAG."
    ),
    version="1.0.0"
)

app.include_router(
    research_router
)


@app.get("/")
def health_check():
    """
    Health check endpoint.

    Returns
    -------
    dict
        Service status.
    """

    return {

        "service": "Research Service",

        "status": "Running"

    }