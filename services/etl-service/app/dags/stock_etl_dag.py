from datetime import datetime, timezone

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="stock_etl",
    start_date = datetime(2025, 1, 1, tzinfo=timezone.utc),
    schedule="@daily",
    catchup=False,
) as dag:

    load_stock_task = BashOperator(
        task_id="load_stock_data",
        bash_command="""
        cd /opt/airflow/etl-service &&
        python -m app.jobs.load_stock_data
        """
    )