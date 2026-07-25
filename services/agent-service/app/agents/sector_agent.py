"""
Sector Agent.

Handles sector-related
requests for the Trading
Research Agent.

The Sector Agent delegates
all sector analysis tasks
to the Sector MCP.
"""

import logging
from typing import Any

from app.exceptions.custom_exceptions import (
    InvalidRequestException,
)
from app.mcp.sector_mcp import SectorMCP

logger = logging.getLogger(__name__)


class SectorAgent:
    """
    Sector Agent.

    Uses the Sector MCP
    to analyze business
    sectors.
    """

    def __init__(self) -> None:
        """
        Initialize the
        Sector MCP.
        """

        logger.info(
            "Initializing Sector Agent."
        )

        self.mcp = SectorMCP()

    # -----------------------------------------------------
    # Default Response
    # -----------------------------------------------------

    def answer(
        self,
        question: str,
        sector: str,
    ) -> dict[str, Any]:
        """
        Handle sector-related
        questions.

        Parameters
        ----------
        question : str
            User question.

        sector : str
            Sector name.

        Returns
        -------
        dict[str, Any]
            Sector response.

        Raises
        ------
        InvalidRequestException
            If the question or sector is empty.
        """

        if not question or not question.strip():

            logger.warning(
                "Empty question received."
            )

            raise InvalidRequestException(
                "Question cannot be empty."
            )

        if not sector or not sector.strip():

            logger.warning(
                "Empty sector received."
            )

            raise InvalidRequestException(
                "Sector cannot be empty."
            )

        question = question.lower()

        logger.info(
            "Processing sector request | sector=%s",
            sector,
        )

        recommendation_keywords = [
            "best",
            "good",
            "top",
            "recommend",
            "recommendation",
            "performing",
            "leader",
            "strong",
            "strongest",
        ]

        company_keywords = [
            "company",
            "companies",
            "list",
            "which companies",
        ]

        news_keywords = [
            "news",
            "headline",
            "headlines",
            "latest",
        ]

        finance_keywords = [
            "stock",
            "price",
            "financial",
            "finance",
            "market",
            "performance",
        ]

        # ---------------------------------------------
        # Best Company Recommendation
        # ---------------------------------------------

        if any(
            keyword in question
            for keyword in recommendation_keywords
        ):

            logger.info(
                "Routing to sector recommendation."
            )

            return {
                "intent": "recommendation",
                **self.mcp.get_sector_summary(
                    sector
                ),
            }

        # ---------------------------------------------
        # Company Listing
        # ---------------------------------------------

        if any(
            keyword in question
            for keyword in company_keywords
        ):

            logger.info(
                "Routing to sector companies."
            )

            return {
                "intent": "companies",
                "sector": sector,
                "companies": self.companies(
                    sector
                ),
            }

        # ---------------------------------------------
        # Sector News
        # ---------------------------------------------

        if any(
            keyword in question
            for keyword in news_keywords
        ):

            logger.info(
                "Routing to sector news."
            )

            return {
                "intent": "news",
                "sector": sector,
                "news": self.mcp.get_sector_news(
                    sector
                ),
            }

        # ---------------------------------------------
        # Sector Finance
        # ---------------------------------------------

        if any(
            keyword in question
            for keyword in finance_keywords
        ):

            logger.info(
                "Routing to sector finance."
            )

            return {
                "intent": "finance",
                "sector": sector,
                "finance": self.mcp.get_sector_finance(
                    sector
                ),
            }

        # ---------------------------------------------
        # Default Sector Summary
        # ---------------------------------------------

        logger.info(
            "Returning sector summary."
        )

        return {
            "intent": "summary",
            **self.summarize(
                sector
            ),
        }

    # -----------------------------------------------------
    # Sector Summary
    # -----------------------------------------------------

    def summarize(
        self,
        sector: str,
    ) -> dict[str, Any]:
        """
        Retrieve sector summary.
        """

        logger.info(
            "Retrieving sector summary | sector=%s",
            sector,
        )

        return self.mcp.get_sector_summary(
            sector
        )

    # -----------------------------------------------------
    # Sector Companies
    # -----------------------------------------------------

    def companies(
        self,
        sector: str,
    ) -> list[dict[str, Any]]:
        """
        Retrieve companies
        belonging to a sector.
        """

        logger.info(
            "Retrieving companies | sector=%s",
            sector,
        )

        return self.mcp.get_sector_companies(
            sector
        )

    # -----------------------------------------------------
    # Health Check
    # -----------------------------------------------------

    def health_check(
        self,
    ) -> dict[str, Any]:
        """
        Check Sector MCP health.

        Returns
        -------
        dict[str, Any]
            Health status.
        """

        logger.info(
            "Sector Agent health check."
        )

        return self.mcp.health_check()


sector_agent = SectorAgent()