"""
Sector MCP.

Provides sector analysis
tools for the Trading
Research Agent.

The Sector MCP orchestrates
Finance, News and Research
MCPs to analyze companies
within a business sector.
"""

import logging
from typing import Any

from app.exceptions.custom_exceptions import (
    InvalidRequestException,
)
from app.mcp.finance_mcp import FinanceMCP
from app.mcp.news_mcp import NewsMCP
from app.mcp.research_mcp import ResearchMCP
from app.repositories.company_repository import CompanyRepository

logger = logging.getLogger(__name__)


class SectorMCP:
    """
    Sector MCP.

    Collects finance,
    news and research
    information for
    companies within
    a sector.
    """

    def __init__(self) -> None:
        """
        Initialize MCPs.
        """

        logger.info(
            "Initializing Sector MCP."
        )

        self.finance = FinanceMCP()
        self.news = NewsMCP()
        self.research = ResearchMCP()
        

    # -----------------------------------------------------
    # Validation
    # -----------------------------------------------------

    @staticmethod
    def _validate_sector(
        sector: str,
    ) -> None:
        """
        Validate sector name.
        """

        if not sector or not sector.strip():

            raise InvalidRequestException(
                "Sector name cannot be empty."
            )

    def get_company_sector(
        self,
        company_name: str,
    ) -> str:
        """
        Retrieve the sector
        for a company.
        """

        logger.info(
            "Fetching sector for company=%s",
            company_name,
        )

        sector = CompanyRepository().get_sector(
        company_name
            )

        if not sector:

            logger.warning(
                "Company not found: %s",
                company_name,
            )

            raise InvalidRequestException(
                f"Company '{company_name}' not found."
            )

        return sector
    # -----------------------------------------------------
    # Sector Companies
    # -----------------------------------------------------

    def get_sector_companies(
        self,
        sector: str,
    ) -> list[str]:
        """
        Return companies
        belonging to a sector.
        """

        self._validate_sector(
            sector
        )

        logger.info(
            "Fetching companies for sector=%s",
            sector,
        )

        return CompanyRepository().get_companies_by_sector(
    sector
        )

    # -----------------------------------------------------
    # Finance
    # -----------------------------------------------------

    def get_sector_finance(
        self,
        sector: str,
    ) -> list[dict[str, Any]]:
        """
        Retrieve financial
        summaries for all
        companies in a sector.
        """

        logger.info(
            "Fetching sector finance | sector=%s",
            sector,
        )

        companies = self.get_sector_companies(
            sector
        )

        finance = []

        for company in companies:

            try:

                finance.append(
                    self.finance.get_stock_summary(
                        company
                    )
                )

            except Exception as ex:

                logger.warning(
                    "Skipping finance for %s: %s",
                    company,
                    ex,
                )

        return finance

    # -----------------------------------------------------
    # News
    # -----------------------------------------------------

    def get_sector_news(
        self,
        sector: str,
    ) -> list[dict[str, Any]]:
        """
        Retrieve news and
        sentiment for all
        companies in a sector.
        """

        logger.info(
            "Fetching sector news | sector=%s",
            sector,
        )

        companies = self.get_sector_companies(
            sector
        )

        news = []

        for company in companies:

            try:

                news.append(
                    {
                        "company": company,
                        "summary": self.news.get_news_summary(
                            company
                        ),
                        "sentiment": self.news.get_latest_sentiment(
                            company
                        ),
                    }
                )

            except Exception as ex:

                logger.warning(
                    "Skipping news for %s: %s",
                    company,
                    ex,
                )

        return news

    # -----------------------------------------------------
    # Research
    # -----------------------------------------------------

    def get_sector_research(
        self,
        sector: str,
    ) -> list[dict[str, Any]]:
        """
        Retrieve research
        summaries for all
        companies in a sector.
        """

        logger.info(
            "Fetching sector research | sector=%s",
            sector,
        )

        companies = self.get_sector_companies(
            sector
        )

        research = []

        for company in companies:

            try:

                result = self.research.answer_question(
                    (
                        f"Provide a concise research summary "
                        f"of {company} in under 150 words "
                        f"covering business, financial "
                        f"performance, growth strategy "
                        f"and risks."
                    )
                )

                research.append(
                    {
                        "company": company,
                        "research": (
                            result.get("answer", "")
                            if isinstance(result, dict)
                            else str(result or "")
                        ),
                    }
                )

            except Exception as ex:

                logger.warning(
                    "Skipping research for %s: %s",
                    company,
                    ex,
                )

        return research

    # -----------------------------------------------------
    # Sector Summary
    # -----------------------------------------------------

    def get_sector_summary(
        self,
        sector: str,
    ) -> dict[str, Any]:
        """
        Retrieve complete
        sector analysis.
        """

        logger.info(
            "Generating sector summary | sector=%s",
            sector,
        )

        companies = self.get_sector_companies(
            sector
        )

        if not companies:

            logger.warning(
                "Sector not found: %s",
                sector,
            )

            raise InvalidRequestException(
                f"Sector '{sector}' not found."
            )

        finance = self.get_sector_finance(
            sector
        )

        news = self.get_sector_news(
            sector
        )

        research = self.get_sector_research(
            sector
        )

        logger.info(
            "Sector summary generated successfully."
        )

        return {
            "sector": sector,
            "total_companies": len(companies),
            "companies": companies,
            "finance": finance,
            "news": news,
            "research": research,
        }

    # -----------------------------------------------------
    # Health Check
    # -----------------------------------------------------

    def health_check(
        self,
    ) -> dict[str, Any]:
        """
        Check MCP availability.
        """

        logger.info(
            "Sector MCP health check."
        )

        return {
            "finance": self.finance.health_check(),
            "news": self.news.health_check(),
            "research": self.research.health_check(),
        }


sector_mcp = SectorMCP()