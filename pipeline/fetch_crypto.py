import requests
import os
from datetime import datetime, timezone
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
    # Fetches Open, High, Low, Close data for a given coin from CoinGecko API
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"
    params = {
        "vs_currency": "usd",
        "days": "1",
        "x_cg_demo_api_key": api_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()  # Fix: was missing return


def fetch_volume(coin_id):
    #Fetches total volume data for a given coin from CoinGecko API
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "1",
        "x_cg_demo_api_key": api_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["total_volumes"][-1][1]


def fetch_coin_row(coin_id, ticker):
    '''Assembles a single price row for a coin, ready to insert into the Prices table'''
    ohlc_data = fetch_ohlc(coin_id)
    volume = fetch_volume(coin_id)

    latest = ohlc_data[-1]  # Most recent OHLC data point
    timestamp, open_price, high_price, low_price, close_price = latest

    # CoinGecko returns Unix milliseconds — convert to a date string for MySQL
    price_date = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).strftime("%Y-%m-%d")

    return {
        "ticker": ticker,
        "price_date": price_date,
        "open_price": open_price,
        "high_price": high_price,
        "low_price": low_price,
        "close_price": close_price,
        "volume": int(volume)
    }




def fetch_volume_history(coin_id):
    """Fetches historical daily volume for a coin. Returns a dict of {date_str: volume}."""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "180",  # ~6 months; adjust as needed
        "x_cg_demo_api_key": api_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Build a date -> volume lookup so fetch_ohlc_history can join on date
    volume_by_date = {}
    for timestamp, volume in data["total_volumes"]:
        date_str = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
        volume_by_date[date_str] = int(volume)

    return volume_by_date


def fetch_ohlc_history(coin_id):
    """Fetches historical OHLCV rows for a coin, joined with volume by date."""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"
    params = {
        "vs_currency": "usd",
        "days": "180",  # Keep in sync with fetch_volume_history
        "x_cg_demo_api_key": api_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    ohlc_data = response.json()

    # Fetch volume history once — not once per row
    volume_by_date = fetch_volume_history(coin_id)

    rows = []
    for entry in ohlc_data:
        timestamp, open_price, high_price, low_price, close_price = entry
        price_date = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).strftime("%Y-%m-%d")

        # Fall back to 0 if a date has OHLC but no matching volume entry
        volume = volume_by_date.get(price_date, 0)

        rows.append({
            "ticker": coins[coin_id],
            "price_date": price_date,
            "open_price": open_price,
            "high_price": high_price,
            "low_price": low_price,
            "close_price": close_price,
            "volume": volume
        })

    return rows

if __name__ == "__main__":
    for coin_id, ticker in coins.items():
        row = fetch_coin_row(coin_id, ticker)
        print(row)