import os
import time
import requests

api_key = "CG-HpY9BMmfvvqA2WciR14ja1UN"

# Double check that the key was actually loaded
if not api_key:
    print("CRITICAL ERROR: 'ALPHA_VANTAGE_API_KEY' environment variable not found.")
    print("Please set it in your terminal or use: api_key = 'YOUR_ACTUAL_KEY'")

stocks = ["AAPL", "GOOGL", "AMZN", "MSFT"]
url = "https://www.alphavantage.co/query"

for stock in stocks:
    params = {
    "function": "TIME_SERIES_DAILY",  # Changed to a free endpoint
    "symbol": stock,
    "apikey": api_key
}
    response = requests.get(url, params=params)
    data = response.json()
    time_series = data.get("Time Series (Daily)", {})
    
    print(f"\n--- {stock} ---")
    if time_series:
        latest_day = list(time_series.keys())[0]
        latest_data = time_series[latest_day]
        print(f"Latest Day: {latest_day}")
        print(f"Latest Price: {latest_data['4. close']}")
        print(f"Latest Volume: {latest_data['5. volume']}")
    else:
        print("No data. Raw response:")
        print(data)
    # Free tier safe delay
    time.sleep(15)
