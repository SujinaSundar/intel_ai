from app.sentiment.sentiment_service import (
    predict_sentiment
)

text = (
    "Infosys beats earnings estimates and raises guidance"
)

label, confidence = predict_sentiment(
    text
)

print(label)
print(confidence)