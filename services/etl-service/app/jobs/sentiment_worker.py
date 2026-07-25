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
"""

import time

from app.core.logger import logger
from app.jobs.generate_sentiment import process_news_sentiment


POLL_INTERVAL = 60  # seconds


def run() -> None:
    """
    Start the continuous sentiment worker.

    Every POLL_INTERVAL seconds the worker scans for
    unprocessed news articles and invokes the FinBERT
    sentiment pipeline.
    """

    logger.info("=" * 80)
    logger.info("Starting Sentiment Worker")
    logger.info("Polling Interval : %d seconds", POLL_INTERVAL)
    logger.info("=" * 80)

    while True:

        try:

            logger.info("Checking for unprocessed news articles...")

            process_news_sentiment()

            logger.info(
                "Sentiment processing cycle completed successfully."
            )

        except Exception:

            logger.exception(
                "Unexpected error during sentiment processing."
            )

        logger.info(
            "Sleeping for %d seconds before next polling cycle.",
            POLL_INTERVAL,
        )

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    run()