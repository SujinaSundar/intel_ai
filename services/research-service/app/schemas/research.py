"""
Research Schemas.

Pydantic request models
for Research Service.
"""

from pydantic import BaseModel


class ResearchRequest(BaseModel):
    """
    Research request.
    """

    question: str