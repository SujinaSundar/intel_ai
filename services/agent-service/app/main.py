"""
Main entry point for the Agent Service.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.auth_router import router as auth_router
from app.core.logger import setup_logging
from app.core.request_logger import log_requests
from app.exceptions.exception_handlers import (
    register_exception_handlers,
)
from app.router.agent import router as agent_router

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
    logger.info("Starting Agent Service...")

    logger.info("Registered Routes:")

    for route in app.routes:
        logger.info(route.path)

    logger.info("=" * 70)

    yield

    logger.info("Shutting down Agent Service.")


# -----------------------------------------------------
# FastAPI Application
# -----------------------------------------------------

app = FastAPI(
    title="Agent Service",
    description="AI-powered Trading Research Agent Service",
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
# Root Endpoint
# -----------------------------------------------------


@app.get(
    "/",
    tags=["Health"],
    summary="Health Check",
)
def root() -> dict[str, str]:
    """
    Health check endpoint.
    """

    return {
        "service": "Agent Service",
        "status": "Running",
    }


# -----------------------------------------------------
# Debug Endpoint
# -----------------------------------------------------


@app.get(
    "/debug",
    tags=["Debug"],
    summary="Registered Routes",
)
def debug() -> dict[str, object]:
    """
    Return all registered routes.

    Intended for development
    purposes only.
    """

    return {
        "message": "Development Debug Endpoint",
        "routes": [
            route.path
            for route in app.routes
        ],
    }


# -----------------------------------------------------
# Routers
# -----------------------------------------------------

app.include_router(auth_router)

app.include_router(agent_router)