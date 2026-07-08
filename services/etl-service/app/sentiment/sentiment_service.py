from app.sentiment.finbert_model import (
    finbert_pipeline
)


def predict_sentiment(
    text: str
) -> tuple[str, float]:

    result = finbert_pipeline(text)[0]

    return (
        result["label"],
        result["score"]
    )