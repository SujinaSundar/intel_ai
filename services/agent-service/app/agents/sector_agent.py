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
        sector: str
    ) -> dict:
        """
        Default response.

        Returns a summary
        of the given sector.

        Parameters
        ----------
        sector : str

        Returns
        -------
        dict
        """

        return self.summarize(
            sector
        )

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