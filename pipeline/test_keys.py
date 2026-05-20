from dotenv import load_dotenv
import os

load_dotenv()

coingecko_key = os.getenv("COINGECKO_API_KEY")
alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY")

print("CoinGecko Key:", coingecko_key)
print("Alpha Vantage Key:", alpha_vantage_key)