import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("COINGECKO_API_KEY")

coins = ["bitcoin", "ethereum", "ripple", "stellar"]

for coin in coins:
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    
    params = {
    "vs_currency": "usd",
    "days": "1",
    "interval": "daily",
    "x_cg_demo_api_key": api_key
}
    
    response = requests.get(url, params=params)
    
    data = response.json()
    prices = data["prices"]
    volumes = data["total_volumes"]
    
    print(f"\n--- {coin.upper()} ---")
    print(f"Latest Price: {prices[-1]}")
    print(f"Latest Volume: {volumes[-1]}")