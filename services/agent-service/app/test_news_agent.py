from pprint import pprint

from app.agents.news_agent import NewsAgent

agent = NewsAgent()

print("\nLatest News")
pprint(
    agent.latest_news(
        "Infosys"
    )
)

print("\nSummary")
pprint(
    agent.summary(
        "Infosys"
    )
)

print("\nPositive News")
pprint(
    agent.positive_news(
        "Infosys"
    )
)