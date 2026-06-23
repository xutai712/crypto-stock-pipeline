import datetime
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

def fetch_stock_history(stock):
    #Fetches OHLCV data from Jan 1st 2026 to now for a given stock from Alpha Vantage and returns a list of rows ready to insert into the Prices table
    # Note: outputsize=full is a premium-only feature on Alpha Vantage's free tier,
    # so we use the default "compact" (last 100 daily points), which covers Jan 1 to now.
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock,
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    # Alpha Vantage returns a "Note" or "Information" key instead of data when rate-limited
    if "Note" in data or "Information" in data:
        msg = data.get("Note") or data.get("Information")
        raise RuntimeError(f"Alpha Vantage rate limit hit for {stock}: {msg}")

    time_series = data.get("Time Series (Daily)", {})
    if not time_series:
        raise RuntimeError(f"No data returned for {stock}. Response keys: {list(data.keys())}")

    start_date = datetime.date(2026, 1, 1)
    rows = []
    for date_str, daily_data in time_series.items():
        if datetime.date.fromisoformat(date_str) >= start_date:
            rows.append({
                "ticker": stock,
                "price_date": date_str,
                "open_price": float(daily_data["1. open"]),
                "high_price": float(daily_data["2. high"]),
                "low_price": float(daily_data["3. low"]),
                "close_price": float(daily_data["4. close"]),
                "volume": int(daily_data["5. volume"])
            })
    return rows

if __name__ == "__main__":
    for stock in stocks:
        row = fetch_stock_row(stock)
        print(row)
        time.sleep(15)  #Alpha Vantage free tier is limited to 5 calls per minute