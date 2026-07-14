"""
Finance Agent

Handles finance-related user requests.
"""

from app.mcp.finance_mcp import FinanceMCP


class FinanceAgent:
    """
    Finance Agent.

    Handles finance-related
    queries for companies.
    """

    def __init__(self):

        self.finance = FinanceMCP()

    def answer(
        self,
        question: str,
        company_name: str
    ):
        """
        Route the finance question
        to the appropriate MCP tool.
        """

        question = question.lower()

        # ---------------------------------
        # Price History
        # ---------------------------------

        if any(
            keyword in question
            for keyword in [
                "history",
                "historical",
                "price history",
                "past prices"
            ]
        ):

            return self.price_history(
                company_name
            )

        # ---------------------------------
        # Trading Volume
        # ---------------------------------

        if any(
            keyword in question
            for keyword in [
                "volume",
                "trading volume"
            ]
        ):

            return self.latest_volume(
                company_name
            )

        # ---------------------------------
        # Stock Summary
        # ---------------------------------

        if any(
            keyword in question
            for keyword in [
                "summary",
                "performance"
            ]
        ):

            return self.stock_summary(
                company_name
            )

        # ---------------------------------
        # Latest Price
        # ---------------------------------

        if any(
            keyword in question
            for keyword in [
                "price",
                "stock price",
                "open",
                "close",
                "high",
                "low"
            ]
        ):

            return self.latest_price(
                company_name
            )

        # ---------------------------------
        # Default
        # ---------------------------------

        return self.stock_summary(
            company_name
        )

    def latest_price(
        self,
        company_name: str
    ):

        return self.finance.get_latest_price(
            company_name
        )

    def stock_summary(
        self,
        company_name: str
    ):

        return self.finance.get_stock_summary(
            company_name
        )

    def latest_volume(
        self,
        company_name: str
    ):

        return self.finance.get_latest_volume(
            company_name
        )

    def price_history(
        self,
        company_name: str,
        limit: int = 5
    ):

        return self.finance.get_price_history(
            company_name,
            limit
        )