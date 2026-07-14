"""
Chat Schemas.

Defines request and
response models for
the Agent Service.
"""

from pydantic import (
    BaseModel
)


class ChatRequest(
    BaseModel
):
    """
    Chat Request.

    Attributes
    ----------
    question : str
        User research
        question.
    """

    question: str


class ChatResponse(
    BaseModel
):
    """
    Chat Response.

    Attributes
    ----------
    answer : str
        Final AI response.
    """

    answer: str