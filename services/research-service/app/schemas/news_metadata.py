"""
Schemas for news metadata.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class NewsMetadataCreate(BaseModel):
    """
    Request model for creating
    news metadata.
    """

    company_id: int = Field(
        description="Company identifier."
    )

    title: str = Field(
        description="News title."
    )

    source: str = Field(
        description="News source."
    )

    url: str = Field(
        description="News article URL."
    )

    published_date: datetime = Field(
        description="Publication date and time."
    )


class NewsMetadataResponse(BaseModel):
    """
    Response model for
    news metadata.
    """

    id: int = Field(
        description="News identifier."
    )

    company_id: int = Field(
        description="Company identifier."
    )

    title: str = Field(
        description="News title."
    )

    source: str = Field(
        description="News source."
    )

    url: str = Field(
        description="News article URL."
    )

    published_date: datetime = Field(
        description="Publication date and time."
    )

    model_config = {
        "from_attributes": True,
    }