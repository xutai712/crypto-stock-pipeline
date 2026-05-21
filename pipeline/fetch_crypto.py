import requests
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("COINGECKO_API_KEY")

coins = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "ripple": "XRP",
    "stellar": "XLM"
}
def fetch_ohlc(coin_id):
    '''Fetches Open, High, Low, Close data for a given coin from CoinGecko API'''
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"
    params = {
        "vs_currency": "usd",
        "days": "1",
        "x_cg_demo_api_key": api_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

def fetch_volume(coin_id):
    '''Fetches total volume data for a given coin from CoinGecko API'''
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "1",
        "x_cg_demo_api_key": api_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["total_volumes"][-1][1]  # Return latest volume

for coin_id, ticker in coins.items():
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    ohlc_data = fetch_ohlc(coin_id)
    volume = fetch_volume(coin_id)

    latest = ohlc_data[-1]  # Get the latest OHLC data point
    timestamp, open_price, high_price, low_price, close_price = latest
    
    print(f"\n--- {ticker} ---")
    print(f"Open:   {open_price}")
    print(f"High:   {high_price}")
    print(f"Low:    {low_price}")
    print(f"Close:  {close_price}")
    print(f"Volume: {volume}")