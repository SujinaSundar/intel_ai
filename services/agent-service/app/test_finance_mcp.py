from pprint import pprint

from app.mcp.finance_mcp import FinanceMCP


finance = FinanceMCP()

print("\nLatest Price")
pprint(
    finance.get_latest_price(
        "Infosys"
    )
)

print("\nLatest Volume")
pprint(
    finance.get_latest_volume(
        "Infosys"
    )
)

print("\nStock Summary")
pprint(
    finance.get_stock_summary(
        "Infosys"
    )
)

print("\nPrice History")
pprint(
    finance.get_price_history(
        "Infosys",
        limit=5
    )
)