from pprint import pprint

from app.agents.finance_agent import FinanceAgent

agent = FinanceAgent()

print("\nLatest Price")
pprint(
    agent.latest_price(
        "Infosys"
    )
)

print("\nSummary")
pprint(
    agent.stock_summary(
        "Infosys"
    )
)

print("\nHistory")
pprint(
    agent.price_history(
        "Infosys"
    )
)