from db_connect import connect
from fetch_crypto import fetch_coin_row, coins
from fetch_stocks import fetch_stock_row, stocks
import time

def load_data():
    conn = connect()
    cursor = conn.cursor()
    # Load stock data
    for stock in stocks:
        row = fetch_stock_row(stock)
        cursor.execute("""
            INSERT INTO Prices (ticker, price_date, open_price, high_price, low_price, close_price, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                open_price = VALUES(open_price),
                high_price = VALUES(high_price),
                low_price = VALUES(low_price),
                close_price = VALUES(close_price),
                volume = VALUES(volume) 
        """, (row["ticker"], row["price_date"], row["open_price"], row["high_price"], row["low_price"], row["close_price"], row["volume"]))
        time.sleep(15)  

    # Load crypto data
    for coin_id, ticker in coins.items():
        row = fetch_coin_row(coin_id, ticker)
        cursor.execute("""
            INSERT INTO Prices (ticker, price_date, open_price, high_price, low_price, close_price, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                open_price = VALUES(open_price),
                high_price = VALUES(high_price),
                low_price = VALUES(low_price),
                close_price = VALUES(close_price),
                volume = VALUES(volume) 
        """, (row["ticker"], row["price_date"], row["open_price"], row["high_price"], row["low_price"], row["close_price"], row["volume"])) 
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_data()