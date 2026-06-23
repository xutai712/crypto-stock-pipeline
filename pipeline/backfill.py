# pipeline/backfill.py
# Run with: python pipeline/backfill.py
import sys
import time
sys.path.append("pipeline")
from db_connect import connect
from fetch_crypto import fetch_ohlc_history, coins
from fetch_stocks import fetch_stock_history, stocks

INSERT_SQL = """
    INSERT INTO Prices (ticker, price_date, open_price, high_price, low_price, close_price, volume)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        open_price = VALUES(open_price),
        high_price = VALUES(high_price),
        low_price = VALUES(low_price),
        close_price = VALUES(close_price),
        volume = VALUES(volume)
"""
def row_to_tuple(row):
    return (
        row["ticker"],
        row["price_date"],
        row["open_price"],
        row["high_price"],
        row["low_price"],
        row["close_price"],
        row["volume"]
    )
def backfill():
    conn = connect()
    cursor = conn.cursor()
    try:
        # --- Stocks ---
        print("Backfilling stocks...")
        for i, stock in enumerate(stocks):
            print(f"  Fetching {stock}...")
            rows = fetch_stock_history(stock)
            for row in rows:
                cursor.execute(INSERT_SQL, row_to_tuple(row))
            conn.commit()
            print(f"  Inserted {len(rows)} rows for {stock}")
            if i < len(stocks) - 1:
                time.sleep(15)  # Alpha Vantage free tier: 5 calls/min
        # --- Crypto ---
        print("Backfilling crypto...")
        coin_items = list(coins.items())
        for i, (coin_id, ticker) in enumerate(coin_items):
            print(f"  Fetching {ticker}...")
            rows = fetch_ohlc_history(coin_id)
            for row in rows:
                cursor.execute(INSERT_SQL, row_to_tuple(row))
            conn.commit()
            print(f"  Inserted {len(rows)} rows for {ticker}")
            if i < len(coin_items) - 1:
                time.sleep(2)
    finally:
        cursor.close()
        conn.close()
    print("Backfill complete.")
    
if __name__ == "__main__":
    backfill()