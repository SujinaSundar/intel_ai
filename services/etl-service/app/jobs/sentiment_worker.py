"""
Background worker for continuous sentiment analysis.

Workflow
--------
Airflow News ETL
        ↓
news_metadata
(is_processed = FALSE)
        ↓
Sentiment Worker
        ↓
FinBERT Sentiment Pipeline
        ↓
sentiment_scores
        ↓
news_metadata.is_processed = TRUE

Purpose
-------
Runs continuously as a background service and periodically
checks for newly ingested news articles that have not yet
been processed by the FinBERT sentiment model.

Only articles where:

    is_processed = FALSE

are analyzed.

This makes the pipeline incremental and ensures that each
article is processed exactly once.

Deployment
----------
Designed to run as a dedicated Docker service:

    intel-ai-sentiment-worker

which is independent of:

- Airflow
- FastAPI Agent
- PostgreSQL
- Neo4j

This separation ensures that failures in sentiment analysis
do not interrupt news ingestion or research workflows.
"""

import logging
import time

from app.jobs.generate_sentiment import process_news_sentiment


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

POLL_INTERVAL = 60  # seconds


def run() -> None:
    """
    Start the continuous sentiment worker.

    Every POLL_INTERVAL seconds the worker scans for
    unprocessed news articles and invokes the FinBERT
    sentiment pipeline.

    The worker runs indefinitely until the process is
    terminated.
    """

    logging.info("Sentiment worker started.")

    while True:

        try:

            process_news_sentiment()

        except Exception:

            logging.exception(
                "Unexpected error while processing sentiment."
            )

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":

    run()