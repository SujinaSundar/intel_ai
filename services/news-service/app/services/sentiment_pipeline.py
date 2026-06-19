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
Sentiment Score
    ↓
sentiment_scores
    ↓
Update news_metadata.is_processed=True
"""

from app.database.connection import SessionLocal

from app.database.models import (
    NewsMetadata,
    SentimentScore
)

from app.sentiment.sentiment_service import (
    predict_sentiment
)


def process_news_sentiment() -> None:
    """
    Process all unprocessed news articles and
    generate sentiment scores using FinBERT.

    Returns
    -------
    None
    """

    print("Starting sentiment pipeline...")

    db = SessionLocal()

    try:

        news_articles = (
            db.query(NewsMetadata)
            .filter(
                NewsMetadata.is_processed == False
            )
            .all()
        )

        print(
            f"Found {len(news_articles)} articles."
        )

        if len(news_articles) == 0:

            print(
                "No new articles found."
            )

            return

        for article in news_articles:

            print(
                f"Processing: {article.title}"
            )

        label, confidence = predict_sentiment(
            article.title
        )

        if label == "positive":
            sentiment_score = confidence

        elif label == "negative":
            sentiment_score = -confidence

        else:
            sentiment_score = 0.0


        sentiment = SentimentScore(
            news_id=article.id,
            company_id=article.company_id,
            sentiment_score=sentiment_score,
            sentiment_label=label,
            confidence_score=confidence
        )

        db.add(sentiment)

        article.is_processed = True

        db.commit()

        print(
            "Sentiment analysis completed successfully."
        )

    except Exception as error:

        db.rollback()

        print(
            f"Error: {error}"
        )

    finally:

        db.close()


if __name__ == "__main__":

    process_news_sentiment()