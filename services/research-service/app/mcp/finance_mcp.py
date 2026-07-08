"""
Finance MCP

Provides financial data tools for AI agents.
"""

from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from app.crud.company import CompanyCRUD
from app.crud.stock_price import StockPriceCRUD


class FinanceMCP:
    """
    Finance MCP

    Acts as the interface between AI agents
    and financial data.
    """

    def __init__(self, db: Session):

        self.company_crud = CompanyCRUD(db)
        self.stock_crud = StockPriceCRUD(db)

    # =====================================================
    # Company
    # =====================================================

    def get_company(self, company_name: str):

        return self.company_crud.get_by_name(company_name)

    def get_company_by_ticker(self, ticker: str):

        return self.company_crud.get_by_ticker(ticker)

    def get_companies(self):

        return self.company_crud.get_all()

    def get_companies_by_sector(self, sector: str):

        return self.company_crud.get_by_sector(sector)

    # =====================================================
    # Stock Prices
    # =====================================================

    def get_latest_stock_price(self, company_id: int):

        return self.stock_crud.get_latest(company_id)

    def get_stock_history(
        self,
        company_id: int,
        limit: int = 30
    ):

        return self.stock_crud.get_history(
            company_id,
            limit
        )

    def get_stock_by_date(
        self,
        company_id: int,
        trade_date: date
    ):

        return self.stock_crud.get_by_date(
            company_id,
            trade_date
        )

    def get_stock_between_dates(
        self,
        company_id: int,
        start_date: date,
        end_date: date
    ):

        return self.stock_crud.get_between_dates(
            company_id,
            start_date,
            end_date
        )

    # =====================================================
    # Business Methods
    # =====================================================

    def get_company_overview(
        self,
        company_name: str
    ) -> Optional[dict]:
        """
        Returns company information together with
        the latest stock price.
        """

        company = self.get_company(company_name)

        if company is None:
            return None

        latest_price = self.get_latest_stock_price(company.id)

        return {
            "company": {
                "id": company.id,
                "company_name": company.company_name,
                "ticker": company.ticker,
                "sector": company.sector,
            },
            "latest_stock_price": (
                {
                    "trade_date": latest_price.trade_date,
                    "open_price": latest_price.open_price,
                    "high_price": latest_price.high_price,
                    "low_price": latest_price.low_price,
                    "close_price": latest_price.close_price,
                    "volume": latest_price.volume,
                }
                if latest_price
                else None
            ),
        }

    def compare_companies(
        self,
        company_one: str,
        company_two: str
    ) -> dict:
        """
        Compare two companies.
        """

        return {
            "company_1": self.get_company_overview(company_one),
            "company_2": self.get_company_overview(company_two),
        }

    def get_sector_overview(
        self,
        sector: str
    ) -> dict:
        """
        Returns all companies belonging to a sector
        together with their latest stock price.
        """

        companies = self.get_companies_by_sector(sector)

        sector_data = []

        for company in companies:

            latest_price = self.get_latest_stock_price(
                company.id
            )

            sector_data.append(
                {
                    "company": {
                        "id": company.id,
                        "company_name": company.company_name,
                        "ticker": company.ticker,
                        "sector": company.sector,
                    },
                    "latest_stock_price": (
                        {
                            "trade_date": latest_price.trade_date,
                            "open_price": latest_price.open_price,
                            "high_price": latest_price.high_price,
                            "low_price": latest_price.low_price,
                            "close_price": latest_price.close_price,
                            "volume": latest_price.volume,
                        }
                        if latest_price
                        else None
                    ),
                }
            )

        return {
            "sector": sector,
            "total_companies": len(sector_data),
            "companies": sector_data,
        }