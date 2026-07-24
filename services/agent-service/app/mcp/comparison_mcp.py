"""
Comparison MCP.

Provides company comparison
tools for the Trading
Research Agent.

The Comparison MCP
orchestrates Finance,
News and Research MCPs
to collect information
for two companies.
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


class ComparisonMCP:
    """
    Comparison MCP.

    Collects financial,
    news and research
    information for
    company comparison.
    """

    def __init__(self) -> None:
        """
        Initialize MCPs.
        """

        logger.info(
            "Initializing Comparison MCP."
        )

        self.finance = FinanceMCP()
        self.news = NewsMCP()
        self.research = ResearchMCP()

    # -----------------------------------------------------
    # Validation
    # -----------------------------------------------------

    @staticmethod
    def _validate_companies(
        company_one: str,
        company_two: str,
    ) -> None:
        """
        Validate company names.
        """

        if not company_one or not company_one.strip():

            raise InvalidRequestException(
                "First company name cannot be empty."
            )

        if not company_two or not company_two.strip():

            raise InvalidRequestException(
                "Second company name cannot be empty."
            )

    # -----------------------------------------------------
    # Finance Comparison
    # -----------------------------------------------------

    def compare_finance(
        self,
        company_one: str,
        company_two: str,
    ) -> dict[str, Any]:
        """
        Compare financial data.
        """

        self._validate_companies(
            company_one,
            company_two,
        )

        logger.info(
            "Comparing finance | %s vs %s",
            company_one,
            company_two,
        )

        return {
            "company_one": self.finance.get_stock_summary(
                company_one
            ),
            "company_two": self.finance.get_stock_summary(
                company_two
            ),
        }

    # -----------------------------------------------------
    # News Comparison
    # -----------------------------------------------------

    def compare_news(
        self,
        company_one: str,
        company_two: str,
    ) -> dict[str, Any]:
        """
        Compare company news.
        """

        self._validate_companies(
            company_one,
            company_two,
        )

        logger.info(
            "Comparing news | %s vs %s",
            company_one,
            company_two,
        )

        return {
            "company_one": {
                "summary": self.news.get_news_summary(
                    company_one
                ),
                "sentiment": self.news.get_latest_sentiment(
                    company_one
                ),
                "latest_news": self.news.get_company_news(
                    company_one
                ),
            },
            "company_two": {
                "summary": self.news.get_news_summary(
                    company_two
                ),
                "sentiment": self.news.get_latest_sentiment(
                    company_two
                ),
                "latest_news": self.news.get_company_news(
                    company_two
                ),
            },
        }

    # -----------------------------------------------------
    # Research Comparison
    # -----------------------------------------------------

    def compare_research(
        self,
        company_one: str,
        company_two: str,
    ) -> dict[str, Any]:
        """
        Compare company research.
        """

        self._validate_companies(
            company_one,
            company_two,
        )

        logger.info(
            "Comparing research | %s vs %s",
            company_one,
            company_two,
        )

        return {
            "company_one": self.research.answer_question(
                f"Summarize {company_one}"
            ),
            "company_two": self.research.answer_question(
                f"Summarize {company_two}"
            ),
        }

    # -----------------------------------------------------
    # Company Comparison
    # -----------------------------------------------------

    def compare_companies(
        self,
        company_one: str,
        company_two: str,
    ) -> dict[str, Any]:
        """
        Compare two companies.
        """

        self._validate_companies(
            company_one,
            company_two,
        )

        logger.info(
            "Starting company comparison | %s vs %s",
            company_one,
            company_two,
        )

        finance = self.compare_finance(
            company_one,
            company_two,
        )

        news = self.compare_news(
            company_one,
            company_two,
        )

        research = self.compare_research(
            company_one,
            company_two,
        )

        logger.info(
            "Company comparison completed successfully."
        )

        return {
            "company_one": {
                "name": company_one,
                "finance": finance["company_one"],
                "news": news["company_one"],
                "research": research["company_one"],
            },
            "company_two": {
                "name": company_two,
                "finance": finance["company_two"],
                "news": news["company_two"],
                "research": research["company_two"],
            },
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
            "Comparison MCP health check."
        )

        return {
            "finance": self.finance.health_check(),
            "news": self.news.health_check(),
            "research": self.research.health_check(),
        }


comparison_mcp = ComparisonMCP()