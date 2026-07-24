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

logger = logging.getLogger(__name__)


SECTOR_COMPANIES: dict[str, list[str]] = {
    "IT": [
        "Infosys",
        "TCS",
        "Wipro",
    ],
    "Banking": [
        "HDFC Bank",
        "ICICI Bank",
    ],
    "Energy": [
        "Reliance Industries",
    ],
}


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

        return SECTOR_COMPANIES.get(
            sector,
            [],
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

        return [
            self.finance.get_stock_summary(
                company
            )
            for company in companies
        ]

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

        return [
            {
                "company": company,
                "summary": self.news.get_news_summary(
                    company
                ),
                "sentiment": self.news.get_latest_sentiment(
                    company
                ),
            }
            for company in companies
        ]

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

        return [
            {
                "company": company,
                "research": self.research.answer_question(
                    f"Summarize {company}"
                ),
            }
            for company in companies
        ]

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