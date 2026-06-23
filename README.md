# crypto-stock-pipeline

A data engineering project that pulls daily price data for cryptocurrency and stocks, stores it in a database, and displays it in an interactive dashboard. Built to develop hands-on skills in ETL pipelines, data warehousing, and dashboard development.

**Crypto**
- BTC (Bitcoin)
- ETH (Ethereum)
- XRP (Ripple)
- XLM (Stellar)

**Stocks**
- AAPL (Apple)
- AMZN (Amazon)
- MSFT (Microsoft)
- GOOGL (Google)

## Project Goals
- Build an automated daily data pipeline
- Store clean, structured data in a database
- Transform and model data using dbt
- Display insights in an interactive dashboard
- Backfill data from 2026-01-01 to date
- Deploy the full pipeline to the cloud

## Planned Tech Stack
- **Python** - data fetching and pipeline scripting
- **MySQL** - database storage
- **dbt** - data transformation and modeling
- **Apache Airflow** - pipeline scheduling and orchestration
- **Docker** - containerization
- **Streamlit** - dashboard and visualization

## Roadmap
- [x] Set up project structure and GitHub repository
- [x] Connect to API and explore raw data
- [x] Design database schema
- [x] Write ETL pipeline script
- [x] Build interactive dashboard with Streamlit
- [ ] Schedule pipeline with Airflow
- [ ] Containerize with Docker
