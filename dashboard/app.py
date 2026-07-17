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

#Table displaying OHLCV for each day
load_dotenv()
def load_data():
    conn = connect()
    query = "SELECT p.ticker, a.name, p.price_date, p.open_price, p.high_price, p.low_price, p.close_price, p.volume FROM Prices p INNER JOIN Assets a ON p.ticker = a.ticker ORDER BY a.asset_type ASC;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df
#Latest daily percentage change per asset (today's close vs yesterday's close)
def load_daily_change():
    conn = connect()
    query = """
    WITH cte_prices AS(
        SELECT ticker,
        close_price,
        LAG(close_price, 1) OVER (PARTITION BY ticker ORDER BY price_date) AS yesterday_close,
        (((close_price/LAG(close_price, 1) OVER (PARTITION BY ticker ORDER BY price_date))-1)*100) AS daily_percentage,
        price_date,
        ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY price_date DESC) AS row_num
        FROM Prices
    )
    SELECT cte.ticker, ROUND(cte.daily_percentage,2) AS Daily_Percent FROM cte_prices cte
    JOIN Assets a ON cte.ticker = a.ticker
    WHERE cte.row_num = 1;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df
#Renders a colored KPI card: green if up, red if down, white if flat
def render_kpi_card(ticker, percent):
    if percent is None or pd.isna(percent):
        color, text = "#FFFFFF", "N/A"
    elif percent > 0:
        color, text = "#2ECC71", f"+{percent:.2f}%"
    elif percent < 0:
        color, text = "#E74C3C", f"{percent:.2f}%"
    else:
        color, text = "#FFFFFF", "0.00%"
    st.markdown(
        f"""
        <div style="border:1px solid #333;border-radius:8px;padding:12px;text-align:center;">
            <div style="font-size:13px;color:#AAAAAA;white-space:nowrap;">{ticker}</div>
            <div style="font-size:16px;font-weight:700;color:{color};white-space:nowrap;">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
def main():
    st.title("Market Dashboard")
    #KPI cards: latest daily % change for every asset
    st.markdown("<h4 style='margin-bottom:8px;'>Daily Change</h4>", unsafe_allow_html=True)
    changes = load_daily_change()
    cols = st.columns(len(changes)) if len(changes) else []
    for col, (_, row) in zip(cols, changes.iterrows()):
        with col:
            render_kpi_card(row["ticker"], row["Daily_Percent"])
    df = load_data()
    ticker = st.selectbox("Select Ticker", sorted(df["ticker"].unique()))
    tab1, tab2 = st.tabs(["Price Over Time", "Daily Summary"]) 
    #Gives the user a graph to view the price history of each asset
    with tab1:
        st.subheader("Price Over Time")
        filtered = df[df["ticker"] == ticker].sort_values("price_date")
        asset_name = filtered["name"].iloc[0] if not filtered.empty else ticker
        fig = px.line(filtered, x="price_date", y="close_price", title=f"{asset_name} Close Price")
        st.plotly_chart(fig, use_container_width=True)
    #Just a table of the daily summary of the selected asset
    with tab2:
        filtered = df[df["ticker"] == ticker].sort_values("price_date")
        st.dataframe(filtered, hide_index=True) 
if __name__ == "__main__":    main()    
