"""
Comparison Agent.

Handles company comparison
requests for the Trading
Research Agent.

The Comparison Agent delegates
all comparison tasks to the
Comparison MCP.
"""

from app.mcp.comparison_mcp import (
    ComparisonMCP
)


class ComparisonAgent:
    """
    Comparison Agent.

    Uses the Comparison MCP
    to compare two companies.
    """

    def __init__(
        self
    ):
        """
        Initialize the
        Comparison Agent.
        """

        self.mcp = ComparisonMCP()

    def compare(
        self,
        company_one: str,
        company_two: str
    ) -> dict:
        """
        Compare two companies.

        Parameters
        ----------
        company_one : str
            First company.

        company_two : str
            Second company.

        Returns
        -------
        dict
            Comparison results.
        """

        return self.mcp.compare_companies(

            company_one,

            company_two

        )

    def health_check(
        self
    ) -> dict:
        """
        Check MCP availability.

        Returns
        -------
        dict
            MCP health status.
        """

        return self.mcp.health_check()