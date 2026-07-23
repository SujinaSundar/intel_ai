"""
Agent Routes.

Provides REST APIs
for the Trading
Research Agent.
"""

import traceback

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from app.auth.dependencies import get_current_user
from app.database.models import User
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from app.services.chat_service import (
    ask_question,
)

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

    try:

        print("=" * 80)
        print("Authenticated User")
        print(f"User ID    : {current_user.id}")
        print(f"User Name  : {current_user.name}")
        print(f"User Email : {current_user.email}")
        print("=" * 80)

        answer = ask_question(
            question=request.question,
            user_id=current_user.id,
        )

        return ChatResponse(
            answer=answer
        )

    except Exception as error:

        print("=" * 100)
        print("AGENT SERVICE ERROR")
        traceback.print_exc()
        print("ERROR:", repr(error))
        print("=" * 100)

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@router.get(
    "/health",
)
def health_check():
    """
    Agent Service
    health check.

    Returns
    -------
    dict
    """

    return {
        "service": "Agent Service",
        "status": "Running",
    }