#To run "streamlit run dashboard/app.py"
import os
import mysql
import streamlit as st
import pandas as pd
import sys
sys.path.append("pipeline")
from db_connect import connect
from dotenv import load_dotenv
import plotly.express as px


load_dotenv()
def load_data():
    conn = connect()
    query = "SELECT p.ticker, p.price_date, p.open_price, p.high_price, p.low_price, p.close_price, p.volume FROM Prices p INNER JOIN Assets a ON p.ticker = a.ticker ORDER BY a.asset_type ASC;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df
def main():
    st.title("Market Dashboard")  
    df = load_data()
    tab1, tab2 = st.tabs(["Price Over Time", "Daily Summary"]) 
    #Gives the user a graph to view the price history of each asset
    with tab1:
        st.subheader("Price Over Time")
        ticker = st.selectbox("Select Ticker", sorted(df["ticker"].unique()))
        filtered = df[df["ticker"] == ticker].sort_values("price_date")
        fig = px.line(filtered, x="price_date", y="close_price", title=f"{ticker} Close Price")
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        st.dataframe(df) 
if __name__ == "__main__":    main()    
