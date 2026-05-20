import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

# Return SQL connector
def connect():
    return mysql.connector.connect(
            host = "localhost",  
            user = "root",
            password = os.getenv("SQL_PASSWORD"),
            database = "market_dashboard"
    )

if __name__ == "__main__":
    conn = connect()
    print("Connection successful:", conn.is_connected())
    conn.close()

