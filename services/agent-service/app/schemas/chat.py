"""
Chat schemas.

Defines request and response
models for the Agent Service.
"""

from pydantic import (
    BaseModel,
    Field,
)

# -----------------------------------------------------
# Chat Request
# -----------------------------------------------------

class ChatRequest(BaseModel):
    """
    Request model for chat queries.
    """

    question: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User question for the AI trading research agent.",
        examples=[
            "Compare Infosys and TCS based on recent financial performance."
        ],
    )


# -----------------------------------------------------
# Chat Response
# -----------------------------------------------------

class ChatResponse(BaseModel):
    """
    Response model returned by the AI agent.
    """

    answer: str = Field(
        ...,
        description="AI-generated response.",
        examples=[
            "Infosys reported stronger revenue growth, while TCS maintained higher operating margins."
        ],
    )