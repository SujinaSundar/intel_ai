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

from app.database.connection import (
    SessionLocal
)

from app.database.models import (
    NewsMetadata,
    SentimentScore
)

from app.sentiment.sentiment_service import (
    predict_sentiment
)


def process_news_sentiment() -> None:
    """
    Process all unprocessed news articles
    and store sentiment scores.
    """

    print()
    print("=" * 80)
    print("STARTING SENTIMENT PIPELINE")
    print("=" * 80)

    db = SessionLocal()
    from sqlalchemy import text

    print("=" * 80)

    print(
        "Database:",
        db.execute(
            text("SELECT current_database()")
        ).scalar()
    )

    print(
        "Total News:",
        db.execute(
            text("SELECT COUNT(*) FROM news_metadata")
        ).scalar()
    )

    print(
        "Unprocessed:",
        db.execute(
            text(
                "SELECT COUNT(*) FROM news_metadata WHERE is_processed = FALSE"
            )
        ).scalar()
    )

    print("=" * 80)
    try:

        news_articles = (

            db.query(
                NewsMetadata
            )

            .filter(
                NewsMetadata.is_processed == False
            )

            .all()

        )

        print(
            f"Found {len(news_articles)} unprocessed articles."
        )

        if not news_articles:

            print(
                "No new articles found."
            )

            return

        processed = 0

        skipped = 0

        for article in news_articles:

            try:

                print()

                print("-" * 80)

                print(
                    f"Processing: {article.title}"
                )

                # -----------------------------------
                # Prevent duplicate sentiment rows
                # -----------------------------------

                existing = (

                    db.query(
                        SentimentScore
                    )

                    .filter(
                        SentimentScore.news_id == article.id
                    )

                    .first()

                )

                if existing:

                    article.is_processed = True

                    db.commit()

                    skipped += 1

                    print(
                        "Already processed."
                    )

                    continue

                # -----------------------------------
                # Predict sentiment
                # -----------------------------------

                label, confidence = (

                    predict_sentiment(
                        article.title
                    )

                )

                # -----------------------------------
                # Save sentiment
                # -----------------------------------

                sentiment = SentimentScore(

                    news_id=article.id,

                    company_id=article.company_id,

                    sentiment_label=label,

                    confidence_score=confidence

                )

                db.add(
                    sentiment
                )

                article.is_processed = True

                db.commit()

                processed += 1

                print(
                    f"Label      : {label}"
                )

                print(
                    f"Confidence : {confidence:.4f}"
                )

            except Exception as error:

                db.rollback()

                print()

                print(
                    f"Failed article ID {article.id}"
                )

                print(
                    error
                )

        print()

        print("=" * 80)
        print("PIPELINE SUMMARY")
        print("=" * 80)

        print(
            f"Processed : {processed}"
        )

        print(
            f"Skipped   : {skipped}"
        )

        print(
            f"Total     : {len(news_articles)}"
        )

        print("=" * 80)

    finally:

        db.close()


if __name__ == "__main__":

    process_news_sentiment()