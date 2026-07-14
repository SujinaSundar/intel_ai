from fastapi import APIRouter

from app.schemas.chat import (
    ChatRequest,
    ChatResponse
)

from app.services.chat_service import ask_question


router = APIRouter(
    prefix="",
    tags=["Agent"]
)


@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest
):
    """
    Main entry point for the frontend.
    """

    answer = ask_question(
        request.question
    )

    return ChatResponse(
        answer=answer
    )