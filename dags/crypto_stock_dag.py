from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys

sys.path.append("/opt/airflow/pipeline")

from load import load_data
with DAG(
    dag_id = "crypto_stock_pipeline",
    start_date = datetime(2026, 6, 1),
    schedule = "0 11 * * *", #Run daily at 11am UTC or 5am CST (Fall/Winter) or 6am CDT (Spring/Summer)
    catchup = False,
) as dag:
    load_prices = PythonOperator(
        task_id = "load_prices",
        python_callable = load_data
    )
