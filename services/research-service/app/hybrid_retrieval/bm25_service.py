"""
BM25 retrieval service.

Workflow
--------
Question
    ↓
Tokenize Query
    ↓
BM25 Search
    ↓
Top K Chunks
"""

from rank_bm25 import BM25Okapi

from app.database.connection import SessionLocal

from app.database.models import (
    DocumentChunk
)


def bm25_retrieve(
    query: str,
    top_k: int = 5
) -> list[str]:
    """
    Retrieve relevant chunks using BM25.

    Parameters
    ----------
    query : str

    top_k : int

    Returns
    -------
    list[str]
    """

    db = SessionLocal()

    try:

        chunks = (
            db.query(
                DocumentChunk
            )
            .all()
        )

        documents = [
            chunk.chunk_text
            for chunk in chunks
        ]

        tokenized_corpus = [

            document.lower().split()

            for document in documents
        ]

        bm25 = BM25Okapi(
            tokenized_corpus
        )

        tokenized_query = (
            query
            .lower()
            .split()
        )

        scores = bm25.get_scores(
            tokenized_query
        )

        ranked_indices = (
            sorted(
                range(len(scores)),
                key=lambda i: scores[i],
                reverse=True
            )
        )[:top_k]

        results = [

            documents[index]

            for index in ranked_indices
        ]

        return results

    finally:

        db.close()