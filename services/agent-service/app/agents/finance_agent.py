"""
Finance Agent.

Handles finance-related
user requests.
"""

import logging
from typing import Any

from app.exceptions.custom_exceptions import (
    InvalidRequestException,
)
from app.mcp.finance_mcp import FinanceMCP

logger = logging.getLogger(__name__)


class FinanceAgent:
    """
    Finance Agent.

    Handles finance-related
    queries for companies.
    """

    def __init__(self) -> None:
        """
        Initialize Finance MCP.
        """

        logger.info(
            "Initializing Finance Agent."
        )

        self.finance = FinanceMCP()

    # ---------------------------------------------------------
    # Main Router
    # ---------------------------------------------------------

    def answer(
        self,
        company_name: str,
        intent: str,
        trade_date: str | None = None,
        limit: int | None = None,
        question: str = "",
    ) -> dict[str, Any]:
        """
        Route a finance request
        based on the detected intent.

        Parameters
        ----------
        company_name : str
            Company name.

        intent : str
            Finance intent.

        trade_date : str | None
            Trading date.

        limit : int | None
            Number of records.

        question : str
            Original user question.

        Returns
        -------
        dict[str, Any]
            Finance response.
        """

        logger.info(
            "Finance request received | intent=%s | company=%s",
            intent,
            company_name,
        )

        if not company_name.strip():

            logger.warning(
                "Empty company name received."
            )

            raise InvalidRequestException(
                "Company name cannot be empty."
            )

        if intent == "latest_price":

            return self.latest_price(
                company_name
            )

        elif intent == "price_by_date":

            if trade_date is None:

                raise InvalidRequestException(
                    "Trade date is required."
                )

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

        logger.error(
            "Unknown finance intent | intent=%s",
            intent,
        )

        raise InvalidRequestException(
            f"Unknown finance intent: {intent}"
        )

    # ---------------------------------------------------------
    # MCP Wrappers
    # ---------------------------------------------------------

    def latest_price(
        self,
        company_name: str,
    ) -> dict[str, Any]:
        """
        Retrieve the latest stock price.
        """

        logger.info(
            "Fetching latest price | company=%s",
            company_name,
        )

        return self.finance.get_latest_price(
            company_name
        )

    def price_by_date(
        self,
        company_name: str,
        trade_date: str,
    ) -> dict[str, Any]:
        """
        Retrieve stock price
        for a specific date.
        """

        logger.info(
            "Fetching price by date | company=%s | date=%s",
            company_name,
            trade_date,
        )

        return self.finance.get_price_by_date(
            company_name,
            trade_date,
        )

    def stock_summary(
        self,
        company_name: str,
    ) -> dict[str, Any]:
        """
        Retrieve stock summary.
        """

        logger.info(
            "Fetching stock summary | company=%s",
            company_name,
        )

        return self.finance.get_stock_summary(
            company_name
        )

    def latest_volume(
        self,
        company_name: str,
    ) -> dict[str, Any]:
        """
        Retrieve latest trading volume.
        """

        logger.info(
            "Fetching latest volume | company=%s",
            company_name,
        )

        return self.finance.get_latest_volume(
            company_name
        )

    def price_history(
        self,
        company_name: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Retrieve historical
        stock prices.
        """

        logger.info(
            "Fetching price history | company=%s | limit=%s",
            company_name,
            limit,
        )

        if limit <= 0:

            raise InvalidRequestException(
                "Limit must be greater than zero."
            )

        return self.finance.get_price_history(
            company_name,
            limit,
        )


finance_agent = FinanceAgent()