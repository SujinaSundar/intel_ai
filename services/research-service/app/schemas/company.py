"""
Response schemas for company APIs.
"""

from pydantic import BaseModel, Field


class CompanyResponse(BaseModel):
    """
    Company response model.
    """

    id: int = Field(
        description="Unique company identifier."
    )

    company_name: str = Field(
        description="Company name."
    )

    sector: str = Field(
        description="Business sector."
    )

    model_config = {
        "from_attributes": True,
    }