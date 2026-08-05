"""
Company Repository.

Provides database access
for company information.
"""

import logging

from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import Company

logger = logging.getLogger(__name__)


class CompanyRepository:
    """
    Repository for company
    database operations.
    """

    def __init__(self) -> None:
        """
        Initialize the
        database session.
        """

        self.db: Session = SessionLocal()

    # -----------------------------------------------------
    # Get Company Sector
    # -----------------------------------------------------

    def get_sector(
        self,
        company_name: str,
    ) -> str | None:
        """
        Retrieve the sector
        for a company.

        Parameters
        ----------
        company_name : str
            Company name.

        Returns
        -------
        str | None
            Sector name if found,
            otherwise None.
        """

        logger.info(
            "Fetching sector for company=%s",
            company_name,
        )

        company = (
            self.db.query(Company)
            .filter(
                Company.company_name.ilike(
                    f"%{company_name}%"
                )
            )
            .first()
        )

        if company:

            logger.info(
                "Sector found | company=%s | sector=%s",
                company.company_name,
                company.sector,
            )

            return company.sector

        logger.warning(
            "Company not found: %s",
            company_name,
        )

        return None

    # -----------------------------------------------------
    # Companies by Sector
    # -----------------------------------------------------

    def get_companies_by_sector(
        self,
        sector: str,
    ) -> list[str]:
        """
        Retrieve companies
        belonging to a sector.

        Parameters
        ----------
        sector : str
            Sector name.

        Returns
        -------
        list[str]
            Company names.
        """

        logger.info(
            "Fetching companies for sector=%s",
            sector,
        )

        companies = (
            self.db.query(Company)
            .filter(
                Company.sector.ilike(
                    f"%{sector}%"
                )
            )
            .all()
        )

        company_names = [
            company.company_name
            for company in companies
        ]

        logger.info(
            "Retrieved %d companies for sector=%s",
            len(company_names),
            sector,
        )

        return company_names