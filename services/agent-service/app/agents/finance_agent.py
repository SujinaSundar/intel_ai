"""
Finance Agent

Handles finance-related user requests.
"""

from app.mcp.finance_mcp import FinanceMCP


class FinanceAgent:

    def __init__(self):

        self.finance = FinanceMCP()

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