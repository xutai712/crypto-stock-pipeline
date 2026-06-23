import requests
import os
import time
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
    """Fetches historical daily volume for a coin. Returns a dict of {date_str: volume}.
    market_chart with days>90 returns daily granularity, so 180 days covers Jan 1 to now.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "180",
        "x_cg_demo_api_key": api_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    volume_by_date = {}
    for timestamp, volume in data["total_volumes"]:
        date_str = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
        volume_by_date[date_str] = int(volume)

    return volume_by_date

def _fetch_ohlc_window(coin_id, days):
    """Fetches one OHLC window. Free tier returns daily candles only for days<=90."""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"
    params = {
        "vs_currency": "usd",
        "days": str(days),
        "x_cg_demo_api_key": api_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def fetch_ohlc_history(coin_id):
    """Fetches daily OHLCV rows for a coin back to Jan 1, 2026.
    CoinGecko free tier only returns daily OHLC for days<=90, so we make two
    back-to-back 90-day calls and merge by date (deduplicating).
    """
    volume_by_date = fetch_volume_history(coin_id)
    # Free tier limitation: days<=90 returns daily candles; days=180 returns weekly.
    # Strategy: fetch days=90 first (daily, recent ~90 days), then days=180 (weekly,
    # covers back to Jan 1) and skip dates already seen. Result: daily for recent
    # data, weekly for Jan–Mar where daily isn't available on the free tier.
    seen_dates = set()
    rows = []
    for days in [90, 180]:
        time.sleep(2)
        for entry in _fetch_ohlc_window(coin_id, days):
            timestamp, open_price, high_price, low_price, close_price = entry
            price_date = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
            if price_date in seen_dates:
                continue
            seen_dates.add(price_date)
            rows.append({
                "ticker": coins[coin_id],
                "price_date": price_date,
                "open_price": open_price,
                "high_price": high_price,
                "low_price": low_price,
                "close_price": close_price,
                "volume": volume_by_date.get(price_date, 0)
            })
    return rows

if __name__ == "__main__":
    for coin_id, ticker in coins.items():
        row = fetch_coin_row(coin_id, ticker)
        print(row)