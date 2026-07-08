"""
News Agent

Handles news-related requests.
"""

from app.mcp.news_mcp import NewsMCP


class NewsAgent:

    def __init__(self):

        self.news = NewsMCP()

    def latest_news(
        self,
        company_name: str
    ):

        return self.news.get_latest_news(
            company_name
        )

    def latest_sentiment(
        self,
        company_name: str
    ):

        return self.news.get_latest_sentiment(
            company_name
        )

    def positive_news(
        self,
        company_name: str
    ):

        return self.news.get_positive_news(
            company_name
        )

    def negative_news(
        self,
        company_name: str
    ):

        return self.news.get_negative_news(
            company_name
        )

    def summary(
        self,
        company_name: str
    ):

        return self.news.get_news_summary(
            company_name
        )

    def search(
        self,
        company_name: str,
        keyword: str
    ):

        return self.news.search_news(
            company_name,
            keyword
        )