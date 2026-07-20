"""
Sector Agent.

Handles sector-related
requests for the Trading
Research Agent.

The Sector Agent delegates
all sector analysis tasks
to the Sector MCP.
"""

from app.mcp.sector_mcp import (
    SectorMCP
)


class SectorAgent:
    """
    Sector Agent.

    Uses the Sector MCP
    to analyze business
    sectors.
    """

    def __init__(
        self
    ):
        """
        Initialize the
        Sector MCP.
        """

        self.mcp = SectorMCP()

    # -----------------------------------------------------
    # Default Response
    # -----------------------------------------------------

    def answer(
        self,
        question: str,
        sector: str
    ) -> dict:
        """
        Handle sector-related
        questions.

        Parameters
        ----------
        question : str

        sector : str

        Returns
        -------
        dict
        """

        question = question.lower()

        recommendation_keywords = [

            "best",
            "good",
            "top",
            "recommend",
            "recommendation",
            "performing",
            "leader",
            "strong",
            "strongest"

        ]

        company_keywords = [

            "company",
            "companies",
            "list",
            "which companies"

        ]

        news_keywords = [

            "news",
            "headline",
            "headlines",
            "latest"

        ]

        finance_keywords = [

            "stock",
            "price",
            "financial",
            "finance",
            "market",
            "performance"

        ]

        # ---------------------------------------------
        # Best Company Recommendation
        # ---------------------------------------------

        if any(
            keyword in question
            for keyword in recommendation_keywords
        ):

            return {

                "intent": "recommendation",

                **self.mcp.get_sector_summary(
                    sector
                )

            }

        # ---------------------------------------------
        # Company Listing
        # ---------------------------------------------

        if any(
            keyword in question
            for keyword in company_keywords
        ):

            return {

                "intent": "companies",

                "sector": sector,

                "companies": self.companies(
                    sector
                )

            }

        # ---------------------------------------------
        # Sector News
        # ---------------------------------------------

        if any(
            keyword in question
            for keyword in news_keywords
        ):

            return {

                "intent": "news",

                "sector": sector,

                "news": self.mcp.get_sector_news(
                    sector
                )

            }

        # ---------------------------------------------
        # Sector Finance
        # ---------------------------------------------

        if any(
            keyword in question
            for keyword in finance_keywords
        ):

            return {

                "intent": "finance",

                "sector": sector,

                "finance": self.mcp.get_sector_finance(
                    sector
                )

            }

        # ---------------------------------------------
        # Default Sector Summary
        # ---------------------------------------------

        return {

            "intent": "summary",

            **self.summarize(
                sector
            )

        }

    # -----------------------------------------------------
    # Sector Summary
    # -----------------------------------------------------

    def summarize(
        self,
        sector: str
    ) -> dict:
        """
        Get sector summary.

        Parameters
        ----------
        sector : str

        Returns
        -------
        dict
        """

        return self.mcp.get_sector_summary(
            sector
        )

    # -----------------------------------------------------
    # Sector Companies
    # -----------------------------------------------------

    def companies(
        self,
        sector: str
    ) -> list:
        """
        Get companies
        belonging to
        a sector.

        Parameters
        ----------
        sector : str

        Returns
        -------
        list
        """

        return self.mcp.get_sector_companies(
            sector
        )

    # -----------------------------------------------------
    # Health Check
    # -----------------------------------------------------

    def health_check(
        self
    ) -> dict:
        """
        Check Sector MCP.

        Returns
        -------
        dict
        """

        return self.mcp.health_check()