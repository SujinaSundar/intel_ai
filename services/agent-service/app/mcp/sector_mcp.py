"""
Sector MCP.

Provides sector analysis
tools for the Trading
Research Agent.

The Sector MCP orchestrates
Finance, News and Research
MCPs to analyze companies
within a business sector.
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


SECTOR_COMPANIES = {

    "IT": [

        "Infosys",

        "TCS",

        "Wipro"

    ],

    "Banking": [

        "HDFC Bank",

        "ICICI Bank"

    ],

    "Energy": [

        "Reliance Industries"

    ]

}


class SectorMCP:
    """
    Sector MCP.

    Collects finance,
    news and research
    information for
    companies within
    a sector.
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
    # Sector Companies
    # -----------------------------------------------------

    def get_sector_companies(
        self,
        sector: str
    ) -> list:
        """
        Return companies
        belonging to a sector.

        Parameters
        ----------
        sector : str

        Returns
        -------
        list
        """

        return SECTOR_COMPANIES.get(

            sector,

            []

        )

    # -----------------------------------------------------
    # Finance
    # -----------------------------------------------------

    def get_sector_finance(
        self,
        sector: str
    ) -> list:
        """
        Get finance summary
        for all companies
        in a sector.

        Parameters
        ----------
        sector : str

        Returns
        -------
        list
        """

        companies = self.get_sector_companies(
            sector
        )

        return [

            self.finance.get_stock_summary(
                company
            )

            for company in companies

        ]

    # -----------------------------------------------------
    # News
    # -----------------------------------------------------

    def get_sector_news(
        self,
        sector: str
    ) -> list:
        """
        Get latest news
        for all companies
        in a sector.

        Parameters
        ----------
        sector : str

        Returns
        -------
        list
        """

        companies = self.get_sector_companies(
            sector
        )

        return [

            {

                "company":

                    company,

                "summary":

                    self.news.get_news_summary(
                        company
                    ),

                "sentiment":

                    self.news.get_latest_sentiment(
                        company
                    )

            }

            for company in companies

        ]

    # -----------------------------------------------------
    # Research
    # -----------------------------------------------------

    def get_sector_research(
        self,
        sector: str
    ) -> list:
        """
        Get research
        summary for all
        companies.

        Parameters
        ----------
        sector : str

        Returns
        -------
        list
        """

        companies = self.get_sector_companies(
            sector
        )

        return [

            {

                "company":

                    company,

                "research":

                    self.research.answer_question(

                        f"Summarize {company}"

                    )

            }

            for company in companies

        ]
        # -----------------------------------------------------
    # Sector Summary
    # -----------------------------------------------------

    def get_sector_summary(
        self,
        sector: str
    ) -> dict:
        """
        Get complete
        sector summary.

        Parameters
        ----------
        sector : str

        Returns
        -------
        dict
            Sector analysis.
        """

        companies = self.get_sector_companies(
            sector
        )

        if len(companies) == 0:

            return {

                "error":

                    "Sector not found."

            }

        finance = self.get_sector_finance(
            sector
        )

        news = self.get_sector_news(
            sector
        )

        research = self.get_sector_research(
            sector
        )

        return {

            "sector":

                sector,

            "total_companies":

                len(companies),

            "companies":

                companies,

            "finance":

                finance,

            "news":

                news,

            "research":

                research

        }

    # -----------------------------------------------------
    # Health Check
    # -----------------------------------------------------

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

        return {

            "finance":

                "Available",

            "news":

                "Available",

            "research":

                self.research.health_check()

        }