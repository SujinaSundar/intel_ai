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
        Comparison MCP.
        """

        self.mcp = ComparisonMCP()

    # -----------------------------------------------------
    # Default Response
    # -----------------------------------------------------

    def answer(
        self,
        company_one: str,
        company_two: str
    ) -> dict:
        """
        Default response.

        Compares two
        companies.

        Parameters
        ----------
        company_one : str

        company_two : str

        Returns
        -------
        dict
        """

        return self.compare(

            company_one,

            company_two

        )

    # -----------------------------------------------------
    # Company Comparison
    # -----------------------------------------------------

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

        company_two : str

        Returns
        -------
        dict
        """

        return self.mcp.compare_companies(

            company_one,

            company_two

        )

    # -----------------------------------------------------
    # Health Check
    # -----------------------------------------------------

    def health_check(
        self
    ) -> dict:
        """
        Check Comparison MCP.

        Returns
        -------
        dict
        """

        return self.mcp.health_check()