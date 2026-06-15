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
    st.dataframe(df) 
    tab1, tab2 = st.tabs(["Price Over Time", "Daily Summary"]) 
    #Gives the user two different views of the data
    with tab1:
        st.subheader("Price Over Time")
    with tab2:
        st.subheader("Daily Summary")
    
if __name__ == "__main__":    main()    

