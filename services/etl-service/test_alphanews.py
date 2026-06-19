"""import requests

from app.database.config import settings

url = (
    "https://www.alphavantage.co/query"
    "?function=NEWS_SENTIMENT"
    "&tickers=INFY"
    f"&apikey={settings.ALPHA_VANTAGE_API_KEY}"
)

response = requests.get(url)

data = response.json()

print(data.keys())
print(data["feed"][0])
print(len(data["feed"]))"""
from app.database.config import settings
import requests

url = (
    "https://www.alphavantage.co/query"
    "?function=NEWS_SENTIMENT"
    "&keywords=Reliance+Industries"
    f"&apikey={settings.ALPHA_VANTAGE_API_KEY}"
)

print("Calling API...")

response = requests.get(url, timeout=30)

print("Response received")

data = response.json()

print(data.keys())
print(len(data.get("feed", [])))

if data.get("feed"):
    print(data["feed"][0]["title"])