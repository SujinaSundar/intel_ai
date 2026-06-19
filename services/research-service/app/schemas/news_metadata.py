from datetime import datetime
from pydantic import BaseModel


class NewsMetadataCreate(BaseModel):
    company_id: int
    title: str
    source: str
    url: str
    published_date: datetime


class NewsMetadataResponse(BaseModel):
    id: int
    company_id: int
    title: str
    source: str
    url: str
    published_date: datetime

    model_config = {
        "from_attributes": True
    }