import os
import time
import requests
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

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
    time.sleep(15) #API has a 5 calls per minute limit
