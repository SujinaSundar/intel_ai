import yfinance as yf

ticker = yf.Ticker("INFY.NS")

data = ticker.history(period="5d")

print(data)