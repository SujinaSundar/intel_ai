from app.database.connection import SessionLocal
from app.mcp.finance_mcp import FinanceMCP


def main():

    db = SessionLocal()

    finance = FinanceMCP(db)

    print("\nCompany")
    print(finance.get_company("Infosys"))

    print("\nAll Companies")
    print(finance.get_companies())

    print("\nSector")
    print(
        finance.get_companies_by_sector(
            "Technology"
        )
    )

    company = finance.get_company("Infosys")

    print("\nLatest Price")
    print(
        finance.get_latest_stock_price(
            company.id
        )
    )

    print("\nOverview")
    print(
        finance.get_company_overview(
            "Infosys"
        )
    )

    print("\nComparison")
    print(
        finance.compare_companies(
            "Infosys",
            "TCS"
        )
    )

    print("\nSector Overview")
    print(
        finance.get_sector_overview(
            "IT"
        )
    )


if __name__ == "__main__":
    main()