from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.models import Company


class CompanyCRUD:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Company).all()

    def get_by_name(self, company_name: str):

        return (
            self.db.query(Company)
            .filter(
                func.lower(Company.company_name)
                == company_name.lower()
            )
            .first()
        )

    def get_by_ticker(self, ticker: str):

        return (
            self.db.query(Company)
            .filter(
                func.lower(Company.ticker)
                == ticker.lower()
            )
            .first()
        )

    def get_by_sector(self, sector: str):

        return (
            self.db.query(Company)
            .filter(
                func.lower(Company.sector)
                == sector.lower()
            )
            .all()
        )