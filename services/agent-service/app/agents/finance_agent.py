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

    # ---------------------------------------------------------
    # Main Router
    # ---------------------------------------------------------

    def answer(
        self,
        company_name: str,
        intent: str,
        trade_date=None,
        limit: int | None = None,
        question: str = "",
    ):

        if intent == "latest_price":

            return self.latest_price(
                company_name
            )

        elif intent == "price_by_date":

            return self.price_by_date(
                company_name,
                trade_date,
            )

        elif intent == "price_history":

            return self.price_history(
                company_name,
                limit or 5,
            )

        elif intent == "latest_volume":

            return self.latest_volume(
                company_name,
            )

        elif intent == "stock_summary":

            return self.stock_summary(
                company_name,
            )

        return {
            "error": f"Unknown finance intent: {intent}"
        }

    # ---------------------------------------------------------
    # MCP Wrappers
    # ---------------------------------------------------------

    def latest_price(
        self,
        company_name: str,
    ):

        return self.finance.get_latest_price(
            company_name
        )

    def price_by_date(
        self,
        company_name: str,
        trade_date,
    ):

        return self.finance.get_price_by_date(
            company_name,
            trade_date,
        )

    def stock_summary(
        self,
        company_name: str,
    ):

        return self.finance.get_stock_summary(
            company_name
        )

    def latest_volume(
        self,
        company_name: str,
    ):

        return self.finance.get_latest_volume(
            company_name
        )

    def price_history(
        self,
        company_name: str,
        limit: int = 5,
    ):

        return self.finance.get_price_history(
            company_name,
            limit,
        )