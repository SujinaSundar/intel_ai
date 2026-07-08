"""
News ETL DAG

Purpose:
--------
Runs the complete News ETL pipeline.

Workflow:
---------
1. Extract news from Alpha Vantage.
2. Validate and filter articles.
3. Remove duplicates.
4. Store news in PostgreSQL.
5. Generate FinBERT sentiment.
6. Store sentiment scores.
7. Mark processed articles.

Schedule:
---------
Runs daily.
"""

from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="news_etl",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["news", "etl", "finbert"],
) as dag:

    # ---------------------------------------
    # Task 1 : Load News
    # ---------------------------------------

    load_news_task = BashOperator(
        task_id="load_news_data",
        bash_command="""
        cd /opt/airflow/etl-service &&
        python -m app.jobs.load_news_data
        """
    )
