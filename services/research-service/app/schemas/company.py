from pydantic import BaseModel


class CompanyResponse(BaseModel):

    id: int
    company_name: str
    sector: str

    model_config = {
        "from_attributes": True
    }