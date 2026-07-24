"""
News Agent.

Handles news-related
requests for the
Trading Research Agent.
"""

import logging
from typing import Any

from app.exceptions.custom_exceptions import (
    InvalidRequestException,
)
from app.mcp.news_mcp import NewsMCP

logger = logging.getLogger(__name__)


class NewsAgent:
    """
    News Agent.

    Provides methods for
    retrieving company
    news and sentiment.
    """

    def __init__(self) -> None:
        """
        Initialize News MCP.
        """

        logger.info(
            "Initializing News Agent."
        )

        self.news = NewsMCP()

    # -----------------------------------------------------
    # Main Router
    # -----------------------------------------------------

    def answer(
        self,
        question: str,
        company_name: str,
    ) -> dict[str, Any]:
        """
        Route the user question
        to the appropriate
        News MCP method.

        Parameters
        ----------
        question : str
            User question.

        company_name : str
            Company name.

        Returns
        -------
        dict[str, Any]
            News response.
        """

        if not company_name.strip():

            logger.warning(
                "Empty company name received."
            )

            raise InvalidRequestException(
                "Company name cannot be empty."
            )

        if not question.strip():

            logger.warning(
                "Empty question received."
            )

            raise InvalidRequestException(
                "Question cannot be empty."
            )

        question = question.lower()

        logger.info(
            "Processing news request | company=%s",
            company_name,
        )

        # ---------------------------------
        # Search News
        # ---------------------------------

        if "search" in question:

            keyword = ""

            words = question.split()

            if "about" in words:

                index = words.index("about")

                if index + 1 < len(words):

                    keyword = words[index + 1]

            if keyword:

                logger.info(
                    "Searching news | keyword=%s",
                    keyword,
                )

                return self.search(
                    company_name,
                    keyword,
                )

        # ---------------------------------
        # Positive News
        # ---------------------------------

        if "positive" in question:

            logger.info(
                "Fetching positive news."
            )

            return self.positive_news(
                company_name
            )

        # ---------------------------------
        # Negative News
        # ---------------------------------

        if "negative" in question:

            logger.info(
                "Fetching negative news."
            )

            return self.negative_news(
                company_name
            )

        # ---------------------------------
        # Latest Sentiment
        # ---------------------------------

        if "sentiment" in question:

            logger.info(
                "Fetching latest sentiment."
            )

            return self.latest_sentiment(
                company_name
            )

        # ---------------------------------
        # Latest News
        # ---------------------------------

        if (
            "latest" in question
            or "headline" in question
            or "news" in question
        ):

            logger.info(
                "Fetching latest news."
            )

            return self.latest_news(
                company_name
            )

        # ---------------------------------
        # Default
        # ---------------------------------

        logger.info(
            "Returning news summary."
        )

        return self.summary(
            company_name
        )

    # -----------------------------------------------------
    # Latest News
    # -----------------------------------------------------

    def latest_news(
        self,
        company_name: str,
    ) -> dict[str, Any]:
        """
        Retrieve latest news
        together with summary.
        """

        logger.info(
            "Retrieving latest news | company=%s",
            company_name,
        )

        return {
            "summary": self.news.get_news_summary(
                company_name
            ),
            "latest_news": self.news.get_latest_news(
                company_name
            ),
        }

    # -----------------------------------------------------
    # Latest Sentiment
    # -----------------------------------------------------

    def latest_sentiment(
        self,
        company_name: str,
    ) -> dict[str, Any]:
        """
        Retrieve latest
        sentiment analysis.
        """

        logger.info(
            "Retrieving latest sentiment | company=%s",
            company_name,
        )

        return {
            "summary": self.news.get_news_summary(
                company_name
            ),
            "latest_sentiment": (
                self.news.get_latest_sentiment(
                    company_name
                )
            ),
        }

    # -----------------------------------------------------
    # Positive News
    # -----------------------------------------------------

    def positive_news(
        self,
        company_name: str,
    ) -> list[dict[str, Any]]:
        """
        Retrieve positive news.
        """

        logger.info(
            "Retrieving positive news | company=%s",
            company_name,
        )

        return self.news.get_positive_news(
            company_name
        )

    # -----------------------------------------------------
    # Negative News
    # -----------------------------------------------------

    def negative_news(
        self,
        company_name: str,
    ) -> list[dict[str, Any]]:
        """
        Retrieve negative news.
        """

        logger.info(
            "Retrieving negative news | company=%s",
            company_name,
        )

        return self.news.get_negative_news(
            company_name
        )

    # -----------------------------------------------------
    # News Summary
    # -----------------------------------------------------

    def summary(
        self,
        company_name: str,
    ) -> dict[str, Any]:
        """
        Retrieve company
        news summary.
        """

        logger.info(
            "Retrieving news summary | company=%s",
            company_name,
        )

        return self.news.get_news_summary(
            company_name
        )

    # -----------------------------------------------------
    # Search News
    # -----------------------------------------------------

    def search(
        self,
        company_name: str,
        keyword: str,
    ) -> list[dict[str, Any]]:
        """
        Search company news.
        """

        if not keyword.strip():

            raise InvalidRequestException(
                "Keyword cannot be empty."
            )

        logger.info(
            "Searching company news | company=%s | keyword=%s",
            company_name,
            keyword,
        )

        return self.news.search_news(
            company_name,
            keyword,
        )

    # -----------------------------------------------------
    # Health Check
    # -----------------------------------------------------

    def health_check(
        self,
    ) -> dict[str, str]:
        """
        Check News Agent health.
        """

        logger.info(
            "News Agent health check."
        )

        return {
            "news_agent": "Available"
        }


news_agent = NewsAgent()