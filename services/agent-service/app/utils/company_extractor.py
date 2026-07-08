"""
Extract company names from user queries.
"""

from app.database.connection import SessionLocal
from app.database.models import Company


class CompanyExtractor:

    def __init__(self):

        self.db = SessionLocal()

        self.company_names = [

            company.company_name

            for company in

            self.db.query(
                Company
            ).all()

        ]

    def __del__(self):

        self.db.close()

    def extract_company(
        self,
        query: str
    ):

        query = query.lower()

        for company in self.company_names:

            if company.lower() in query:

                return company

        return None