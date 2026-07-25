"""
Research Service.

Exposes APIs for
Hybrid GraphRAG retrieval.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logger import setup_logging
from app.core.request_logger import log_requests
from app.exceptions.exception_handlers import (
    register_exception_handlers,
)
from app.graph_rag.neo4j_service import (
    close_driver,
    get_driver,
)
from app.routes.research import (
    router as research_router,
)

# -----------------------------------------------------
# Configure Logging
# -----------------------------------------------------

setup_logging()

logger = logging.getLogger(__name__)

# -----------------------------------------------------
# Application Lifespan
# -----------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup
    and shutdown events.
    """

    logger.info("=" * 70)
    logger.info("Starting Research Service...")

    # Initialize Neo4j connection
    get_driver()

    logger.info("Neo4j driver initialized.")

    logger.info("Registered Routes:")

    for route in app.routes:
        logger.info(route.path)

    logger.info("=" * 70)

    yield

    logger.info("Shutting down Research Service.")

    # Close Neo4j connection
    close_driver()

    logger.info("Neo4j driver closed.")


# -----------------------------------------------------
# FastAPI Application
# -----------------------------------------------------

app = FastAPI(
    title="Research Service",
    description=(
        "Provides research retrieval "
        "using Hybrid GraphRAG."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# -----------------------------------------------------
# Exception Handlers
# -----------------------------------------------------

register_exception_handlers(app)

# -----------------------------------------------------
# Middleware
# -----------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(log_requests)

# -----------------------------------------------------
# Routers
# -----------------------------------------------------

app.include_router(research_router)

# -----------------------------------------------------
# Root Endpoint
# -----------------------------------------------------


@app.get(
    "/",
    tags=["Health"],
    summary="Health Check",
)
def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Returns
    -------
    dict[str, str]
        Service status.
    """

    return {
        "service": "Research Service",
        "status": "Running",
    }