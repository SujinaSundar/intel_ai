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
        Sector Agent.
        """

        self.mcp = SectorMCP()

    def summarize(
        self,
        sector: str
    ) -> dict:
        """
        Get sector summary.

        Parameters
        ----------
        sector : str
            Business sector.

        Returns
        -------
        dict
            Sector analysis.
        """

        return self.mcp.get_sector_summary(
            sector
        )

    def companies(
        self,
        sector: str
    ) -> list:
        """
        Get companies
        in a sector.

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

    def health_check(
        self
    ) -> dict:
        """
        Check MCP status.

        Returns
        -------
        dict
            MCP availability.
        """

        return self.mcp.health_check()