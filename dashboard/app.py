#To run "streamlit run dashboard/app.py"
import os
import mysql
import streamlit as st
import pandas as pd
import sys
sys.path.append("pipeline")
from db_connect import connect
from dotenv import load_dotenv


load_dotenv()
def load_data():
    conn = connect()
    query = "SELECT * FROM Prices"
    df = pd.read_sql(query, conn)
    conn.close()
    return df
def main():
    st.title("Market Dashboard")
    df = load_data()
    st.dataframe(df)   
if __name__ == "__main__":    main()    

