from pprint import pprint

from app.mcp.news_mcp import NewsMCP

news = NewsMCP()

print("\nLatest News")
pprint(
    news.get_latest_news(
        "Infosys"
    )
)

print("\nLatest Sentiment")
pprint(
    news.get_latest_sentiment(
        "Infosys"
    )
)

print("\nPositive News")
pprint(
    news.get_positive_news(
        "Infosys"
    )
)

print("\nNegative News")
pprint(
    news.get_negative_news(
        "Infosys"
    )
)

print("\nSummary")
pprint(
    news.get_news_summary(
        "Infosys"
    )
)