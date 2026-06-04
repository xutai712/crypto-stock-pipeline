from datetime import datetime
import os
import time
import requests
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

stocks = ["AAPL", "GOOGL", "AMZN", "MSFT"]
url = "https://www.alphavantage.co/query"

def fetch_stock_row(stock):
    params = {
        "function": "TIME_SERIES_DAILY",  # Changed to a free endpoint
        "symbol": stock,
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    time_series = data.get("Time Series (Daily)", {})
    latest_day = list(time_series.keys())[0]
    latest_data = time_series[latest_day]
    print(latest_data)


    