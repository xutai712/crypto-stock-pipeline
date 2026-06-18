import os
import time
import requests
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

stocks = ["AAPL", "GOOGL", "AMZN", "MSFT"]
url = "https://www.alphavantage.co/query"

def fetch_stock_row(stock):
    '''Fetches OHLCV data for a given stock from Alpha Vantage and returns a row ready to insert into the Prices table'''
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock,
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    time_series = data.get("Time Series (Daily)", {})

    latest_day = list(time_series.keys())[0]  #Alpha Vantage returns date string directly e.g. "2025-06-01"
    latest_data = time_series[latest_day]

    return {
        "ticker": stock,
        "price_date": latest_day,       #Already a clean date string, no conversion needed
        "open_price": float(latest_data["1. open"]),
        "high_price": float(latest_data["2. high"]),
        "low_price": float(latest_data["3. low"]),
        "close_price": float(latest_data["4. close"]),
        "volume": int(latest_data["5. volume"])
    }

if __name__ == "__main__":
    for stock in stocks:
        row = fetch_stock_row(stock)
        print(row)
        time.sleep(15)  #Alpha Vantage free tier is limited to 5 calls per minute