
"""
News ETL DAG

Purpose:
--------
This DAG runs the News ETL pipeline daily.

Workflow:
---------
1. Extract news from Alpha Vantage.
2. Validate data.
3. Remove duplicate records.
4. Load data into PostgreSQL.

Schedule:
---------
Runs daily at 7:00 AM IST.
"""

from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="news_etl",
     start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["news", "etl"],
) as dag:

    load_news_task = BashOperator(
        task_id="load_news_data",
        bash_command="""
        cd /opt/airflow/etl-service &&
        python -m app.jobs.load_news_data
        """
    )

    load_news_task

