"""
Agent Routes.

Provides REST APIs
for the Trading
Research Agent.
"""

import logging

from app.auth.dependencies import get_current_user
from app.database.models import User
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from app.services.chat_service import ask_question
from fastapi import (
    APIRouter,
    Depends,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Agent"]
)


# ---------------------------------------------------------
# Ask Question
# ---------------------------------------------------------

@router.post(
    "/ask",
    response_model=ChatResponse,
)
def ask(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Ask a question to the AI Trading Research Agent.

    Requires JWT authentication.
    """

    logger.info(
        "Processing chat request | user_id=%s | email=%s",
        current_user.id,
        current_user.email,
    )

    answer = ask_question(
        question=request.question,
        user_id=current_user.id,
    )

    logger.info(
        "Chat request completed successfully | user_id=%s",
        current_user.id,
    )

    return ChatResponse(
        answer=answer
    )


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@router.get("/health")
def health_check():
    """
    Agent Service health check.
    """

    logger.info("Health check endpoint accessed.")

    return {
        "service": "Agent Service",
        "status": "Running",
    }