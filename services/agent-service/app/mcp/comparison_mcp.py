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

        self._validate_companies(
            company_one,
            company_two,
        )

        logger.info(
            "Comparing news | %s vs %s",
            company_one,
            company_two,
        )

        company_one_news = (
            self.news.get_company_news(
                company_one
            )
            or []
        )

        company_two_news = (
            self.news.get_company_news(
                company_two
            )
            or []
        )

        return {
            "company_one": {
                "summary": self.news.get_news_summary(
                    company_one
                ),
                "sentiment": self.news.get_latest_sentiment(
                    company_one
                ),
                "latest_news": company_one_news[:3],
            },
            "company_two": {
                "summary": self.news.get_news_summary(
                    company_two
                ),
                "sentiment": self.news.get_latest_sentiment(
                    company_two
                ),
                "latest_news": company_two_news[:3],
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

        self._validate_companies(
            company_one,
            company_two,
        )

        logger.info(
            "Comparing research | %s vs %s",
            company_one,
            company_two,
        )

        research_one = self.research.answer_question(
            (
                f"Provide a concise research summary of "
                f"{company_one} in under 150 words covering "
                f"business, financial performance, growth "
                f"strategy and risks."
            )
        )

        research_two = self.research.answer_question(
            (
                f"Provide a concise research summary of "
                f"{company_two} in under 150 words covering "
                f"business, financial performance, growth "
                f"strategy and risks."
            )
        )

        return {
            "company_one": (
                research_one.get(
                    "answer",
                    "",
                )
                if isinstance(
                    research_one,
                    dict,
                )
                else str(
                    research_one or ""
                )
            ),
            "company_two": (
                research_two.get(
                    "answer",
                    "",
                )
                if isinstance(
                    research_two,
                    dict,
                )
                else str(
                    research_two or ""
                )
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

        logger.info(
            "Comparison MCP health check."
        )

        return {
            "finance": self.finance.health_check(),
            "news": self.news.health_check(),
            "research": self.research.health_check(),
        }


comparison_mcp = ComparisonMCP()