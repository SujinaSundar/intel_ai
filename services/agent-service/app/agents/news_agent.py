"""
News Agent.

Handles news-related
requests for the
Trading Research Agent.
"""

from app.mcp.news_mcp import (
    NewsMCP
)


class NewsAgent:
    """
    News Agent.

    Provides methods for
    retrieving company
    news and sentiment.
    """

    def __init__(
        self
    ):
        """
        Initialize News MCP.
        """

        self.news = NewsMCP()

    # -----------------------------------------------------
    # Default Response
    # -----------------------------------------------------

    def answer(
        self,
        question: str,
        company_name: str
    ):
        """
        Route the user question
        to the appropriate News MCP.
        """

        question = question.lower()

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

                return self.search(
                    company_name,
                    keyword
                )

        # ---------------------------------
        # Positive News
        # ---------------------------------

        if "positive" in question:

            return self.positive_news(
                company_name
            )

        # ---------------------------------
        # Negative News
        # ---------------------------------

        if "negative" in question:

            return self.negative_news(
                company_name
            )

        # ---------------------------------
        # Latest Sentiment
        # ---------------------------------

        if "sentiment" in question:

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

            return self.latest_news(
                company_name
            )

        # ---------------------------------
        # Default
        # ---------------------------------

        return self.summary(
            company_name
        )

    # -----------------------------------------------------
    # Latest News
    # -----------------------------------------------------

    def latest_news(
        self,
        company_name: str
    ):
        """
        Get latest news.
        """

        return self.news.get_latest_news(
            company_name
        )

    # -----------------------------------------------------
    # Latest Sentiment
    # -----------------------------------------------------

    def latest_sentiment(
        self,
        company_name: str
    ):
        """
        Get latest sentiment.
        """

        return self.news.get_latest_sentiment(
            company_name
        )

    # -----------------------------------------------------
    # Positive News
    # -----------------------------------------------------

    def positive_news(
        self,
        company_name: str
    ):
        """
        Get positive news.
        """

        return self.news.get_positive_news(
            company_name
        )

    # -----------------------------------------------------
    # Negative News
    # -----------------------------------------------------

    def negative_news(
        self,
        company_name: str
    ):
        """
        Get negative news.
        """

        return self.news.get_negative_news(
            company_name
        )

    # -----------------------------------------------------
    # News Summary
    # -----------------------------------------------------

    def summary(
        self,
        company_name: str
    ):
        """
        Get news summary.
        """

        return self.news.get_news_summary(
            company_name
        )

    # -----------------------------------------------------
    # Search News
    # -----------------------------------------------------

    def search(
        self,
        company_name: str,
        keyword: str
    ):
        """
        Search company news.
        """

        return self.news.search_news(
            company_name,
            keyword
        )

    # -----------------------------------------------------
    # Health Check
    # -----------------------------------------------------

    def health_check(
        self
    ):
        """
        Check Agent status.
        """

        return {

            "news_agent":

                "Available"

        }