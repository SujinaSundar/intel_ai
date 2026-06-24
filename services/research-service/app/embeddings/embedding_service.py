"""
Embedding service.
"""

from app.embeddings.embedding_model import (
    embedding_model
)


def generate_embedding(
    text: str
) -> list[float]:

    embedding = embedding_model.encode(
        text
    )

    return embedding.tolist()