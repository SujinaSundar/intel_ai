"""
Sentiment analysis pipeline.

Workflow
--------
news_metadata
    ↓
Unprocessed Articles
    ↓
FinBERT
    ↓
Sentiment Label + Confidence
    ↓
sentiment_scores
    ↓
Update news_metadata.is_processed=True
"""

from sqlalchemy import text

from app.core.logger import logger
from app.database.connection import SessionLocal
from app.database.models import (
    NewsMetadata,
    SentimentScore,
)
from app.sentiment.sentiment_service import (
    predict_sentiment,
)


def process_news_sentiment() -> None:
    """
    Process all unprocessed news articles
    and store sentiment scores.
    """

    logger.info("=" * 80)
    logger.info("Starting Sentiment Pipeline")
    logger.info("=" * 80)

    db = SessionLocal()

    try:

        database_name = db.execute(
            text("SELECT current_database()")
        ).scalar()

        total_news = db.execute(
            text("SELECT COUNT(*) FROM news_metadata")
        ).scalar()

        unprocessed_news = db.execute(
            text(
                "SELECT COUNT(*) FROM news_metadata "
                "WHERE is_processed = FALSE"
            )
        ).scalar()

        logger.info("Database              : %s", database_name)
        logger.info("Total News Articles   : %d", total_news)
        logger.info("Unprocessed Articles  : %d", unprocessed_news)

        news_articles = (
            db.query(NewsMetadata)
            .filter(NewsMetadata.is_processed == False)
            .all()
        )

        logger.info(
            "Found %d unprocessed articles.",
            len(news_articles),
        )

        if not news_articles:

            logger.info(
                "No new articles found. Sentiment pipeline finished."
            )

            return

        processed = 0
        skipped = 0

        for article in news_articles:

            try:

                logger.info(
                    "Processing News ID=%s",
                    article.id,
                )

                logger.debug(
                    "Title: %s",
                    article.title,
                )

                # -----------------------------------
                # Prevent duplicate sentiment rows
                # -----------------------------------

                existing = (
                    db.query(SentimentScore)
                    .filter(
                        SentimentScore.news_id == article.id
                    )
                    .first()
                )

                if existing:

                    article.is_processed = True

                    db.commit()

                    skipped += 1

                    logger.debug(
                        "Sentiment already exists for News ID=%s",
                        article.id,
                    )

                    continue

                # -----------------------------------
                # Predict sentiment
                # -----------------------------------

                label, confidence = predict_sentiment(
                    article.title
                )

                logger.info(
                    "Predicted Sentiment=%s Confidence=%.4f",
                    label,
                    confidence,
                )

                # -----------------------------------
                # Save sentiment
                # -----------------------------------

                sentiment = SentimentScore(
                    news_id=article.id,
                    company_id=article.company_id,
                    sentiment_label=label,
                    confidence_score=confidence,
                )

                db.add(sentiment)

                article.is_processed = True

                db.commit()

                processed += 1

                logger.info(
                    "Saved sentiment for News ID=%s",
                    article.id,
                )

            except Exception:

                db.rollback()

                logger.exception(
                    "Failed to process News ID=%s",
                    article.id,
                )

        logger.info("=" * 80)
        logger.info("Sentiment Pipeline Summary")
        logger.info("Processed : %d", processed)
        logger.info("Skipped   : %d", skipped)
        logger.info("Total     : %d", len(news_articles))
        logger.info("=" * 80)

    except Exception:

        db.rollback()

        logger.exception(
            "Sentiment pipeline failed."
        )

        raise

    finally:

        db.close()

        logger.info("Database session closed.")


if __name__ == "__main__":
    process_news_sentiment()