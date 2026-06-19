from app.database.connection import SessionLocal
from app.database.models import Company


companies = [
    {"company_name": "Reliance Industries", "ticker": "RELIANCE.NS", "sector": "Energy"},
    {"company_name": "TCS", "ticker": "TCS.NS", "sector": "IT"},
    {"company_name": "Infosys", "ticker": "INFY.NS", "sector": "IT"},
    {"company_name": "HDFC Bank", "ticker": "HDFCBANK.NS", "sector": "Banking"},
    {"company_name": "ICICI Bank", "ticker": "ICICIBANK.NS", "sector": "Banking"},
    {"company_name": "Bharti Airtel", "ticker": "BHARTIARTL.NS", "sector": "Telecom"},
    {"company_name": "ITC", "ticker": "ITC.NS", "sector": "FMCG"},
    {"company_name": "Larsen & Toubro", "ticker": "LT.NS", "sector": "Infrastructure"},
    {"company_name": "State Bank of India", "ticker": "SBIN.NS", "sector": "Banking"},
    {"company_name": "Axis Bank", "ticker": "AXISBANK.NS", "sector": "Banking"},
]

db = SessionLocal()

for item in companies:

    existing = db.query(Company).filter(
        Company.ticker == item["ticker"]
    ).first()

    if existing:
        continue

    db.add(
        Company(
            company_name=item["company_name"],
            ticker=item["ticker"],
            sector=item["sector"]
        )
    )

db.commit()
db.close()

print("Companies seeded")