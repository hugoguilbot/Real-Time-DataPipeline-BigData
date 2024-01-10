from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from stream_to_kafka import start_streaming


start_date = datetime(2023, 12, 29, 12, 22)

default_args = {
    'owner': 'airflow',
    'start_date': start_date,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

with DAG('companies_created', 
         default_args=default_args, 
         schedule_interval="@continuous", 
         max_active_runs=1,
         catchup=False) as dag:


    data_stream_task = PythonOperator(
    task_id='stream_data_from_api',
    python_callable=start_streaming
    )

    data_stream_task