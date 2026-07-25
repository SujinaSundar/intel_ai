"""
Research Schemas.

Pydantic request models
for Research Service.
"""

from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    """
    Research request.
    """

    question: str = Field(
        description="Research question from the user."
    )