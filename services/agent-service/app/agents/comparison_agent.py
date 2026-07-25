"""
Comparison Agent.

Handles company comparison
requests for the Trading
Research Agent.

The Comparison Agent delegates
all comparison tasks to the
Comparison MCP.
"""

import logging
from typing import Any

from app.exceptions.custom_exceptions import (
    InvalidRequestException,
)
from app.mcp.comparison_mcp import ComparisonMCP

logger = logging.getLogger(__name__)


class ComparisonAgent:
    """
    Comparison Agent.

    Uses the Comparison MCP
    to compare two companies.
    """

    def __init__(self) -> None:
        """
        Initialize the
        Comparison MCP.
        """

        logger.info(
            "Initializing Comparison Agent."
        )

        self.mcp = ComparisonMCP()

    # -----------------------------------------------------
    # Default Response
    # -----------------------------------------------------

    def answer(
        self,
        company_one: str,
        company_two: str,
    ) -> dict[str, Any]:
        """
        Compare two companies.

        Parameters
        ----------
        company_one : str
            First company name.

        company_two : str
            Second company name.

        Returns
        -------
        dict[str, Any]
            Comparison results.

        Raises
        ------
        InvalidRequestException
            If either company name is empty.
        """

        if not company_one or not company_one.strip():

            logger.warning(
                "First company name is empty."
            )

            raise InvalidRequestException(
                "First company name cannot be empty."
            )

        if not company_two or not company_two.strip():

            logger.warning(
                "Second company name is empty."
            )

            raise InvalidRequestException(
                "Second company name cannot be empty."
            )

        logger.info(
            "Processing comparison request | company_one=%s | company_two=%s",
            company_one,
            company_two,
        )

        return self.compare(
            company_one,
            company_two,
        )

    # -----------------------------------------------------
    # Company Comparison
    # -----------------------------------------------------

    def compare(
        self,
        company_one: str,
        company_two: str,
    ) -> dict[str, Any]:
        """
        Compare two companies.

        Parameters
        ----------
        company_one : str
            First company name.

        company_two : str
            Second company name.

        Returns
        -------
        dict[str, Any]
            Comparison results.
        """

        logger.info(
            "Comparing companies | company_one=%s | company_two=%s",
            company_one,
            company_two,
        )

        return self.mcp.compare_companies(
            company_one,
            company_two,
        )

    # -----------------------------------------------------
    # Health Check
    # -----------------------------------------------------

    def health_check(
        self,
    ) -> dict[str, Any]:
        """
        Check Comparison MCP health.

        Returns
        -------
        dict[str, Any]
            Health status.
        """

        logger.info(
            "Comparison Agent health check."
        )

        return self.mcp.health_check()


comparison_agent = ComparisonAgent()