"""
Load FinBERT model.
"""

from transformers import pipeline

finbert_pipeline = pipeline(
    task="text-classification",
    model="ProsusAI/finbert"
)