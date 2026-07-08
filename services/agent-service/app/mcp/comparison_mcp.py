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

from app.mcp.finance_mcp import (
    FinanceMCP
)

from app.mcp.news_mcp import (
    NewsMCP
)

from app.mcp.research_mcp import (
    ResearchMCP
)


class ComparisonMCP:
    """
    Comparison MCP.

    Collects financial,
    news and research
    information for
    company comparison.
    """

    def __init__(
        self
    ):
        """
        Initialize MCPs.
        """

        self.finance = FinanceMCP()

        self.news = NewsMCP()

        self.research = ResearchMCP()

    # -----------------------------------------------------
    # Finance Comparison
    # -----------------------------------------------------

    def compare_finance(
        self,
        company_one: str,
        company_two: str
    ) -> dict:
        """
        Compare financial data.

        Parameters
        ----------
        company_one : str

        company_two : str

        Returns
        -------
        dict
        """

        return {

            "company_one":

                self.finance.get_stock_summary(
                    company_one
                ),

            "company_two":

                self.finance.get_stock_summary(
                    company_two
                )

        }

    # -----------------------------------------------------
    # News Comparison
    # -----------------------------------------------------

    def compare_news(
        self,
        company_one: str,
        company_two: str
    ) -> dict:
        """
        Compare news and
        sentiment.

        Parameters
        ----------
        company_one : str

        company_two : str

        Returns
        -------
        dict
        """

        return {

            "company_one": {

                "summary":

                    self.news.get_news_summary(
                        company_one
                    ),

                "sentiment":

                    self.news.get_latest_sentiment(
                        company_one
                    ),

                "latest_news":

                    self.news.get_company_news(
                        company_one
                    )

            },

            "company_two": {

                "summary":

                    self.news.get_news_summary(
                        company_two
                    ),

                "sentiment":

                    self.news.get_latest_sentiment(
                        company_two
                    ),

                "latest_news":

                    self.news.get_company_news(
                        company_two
                    )

            }

        }

    # -----------------------------------------------------
    # Research Comparison
    # -----------------------------------------------------

    def compare_research(
        self,
        company_one: str,
        company_two: str
    ) -> dict:
        """
        Compare research
        information.

        Parameters
        ----------
        company_one : str

        company_two : str

        Returns
        -------
        dict
        """

        return {

            "company_one":

                self.research.answer_question(

                    f"Summarize {company_one}"

                ),

            "company_two":

                self.research.answer_question(

                    f"Summarize {company_two}"

                )

        }
        # -----------------------------------------------------
    # Company Comparison
    # -----------------------------------------------------

    def compare_companies(
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
            Combined comparison
            information.
        """

        finance = self.compare_finance(

            company_one,

            company_two

        )

        news = self.compare_news(

            company_one,

            company_two

        )

        research = self.compare_research(

            company_one,

            company_two

        )

        return {

            "company_one": {

                "name":

                    company_one,

                "finance":

                    finance["company_one"],

                "news":

                    news["company_one"],

                "research":

                    research["company_one"]

            },

            "company_two": {

                "name":

                    company_two,

                "finance":

                    finance["company_two"],

                "news":

                    news["company_two"],

                "research":

                    research["company_two"]

            }

        }

    # -----------------------------------------------------
    # Health Check
    # -----------------------------------------------------

    def health_check(
        self
    ) -> dict:
        """
        Check MCP availability.

        Returns
        -------
        dict
            MCP status.
        """

        return {

            "finance":

                "Available",

            "news":

                "Available",

            "research":

                self.research.health_check()

        }