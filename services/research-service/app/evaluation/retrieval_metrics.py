"""
Retrieval evaluation metrics.
"""

from app.evaluation.embedding_similarity import (
    compute_similarity
)


SIMILARITY_THRESHOLD = 0.70


def relevance_scores(
    retrieved_documents: list[str],
    ground_truth: str
) -> list[float]:
    """
    Compute similarity scores between
    retrieved documents and ground truth.
    """

    return [

        compute_similarity(
            document,
            ground_truth
        )

        for document in retrieved_documents

    ]


def hit_rate(
    retrieved_documents: list[str],
    ground_truth: str
) -> float:
    """
    Hit Rate.
    """

    scores = relevance_scores(

        retrieved_documents,

        ground_truth

    )

    return float(

        any(
            score >= SIMILARITY_THRESHOLD
            for score in scores
        )

    )


def precision_at_k(
    retrieved_documents: list[str],
    ground_truth: str
) -> float:
    """
    Precision@k.
    """

    if not retrieved_documents:

        return 0.0

    scores = relevance_scores(

        retrieved_documents,

        ground_truth

    )

    relevant = sum(

        score >= SIMILARITY_THRESHOLD

        for score in scores

    )

    return relevant / len(
        retrieved_documents
    )


def recall_at_k(
    retrieved_documents: list[str],
    ground_truth: str
) -> float:
    """
    Recall@k.

    Since there is one ground-truth answer,
    recall becomes 1 if at least one relevant
    chunk is retrieved.
    """

    scores = relevance_scores(

        retrieved_documents,

        ground_truth

    )

    return float(

        any(
            score >= SIMILARITY_THRESHOLD
            for score in scores
        )

    )


def mean_reciprocal_rank(
    retrieved_documents: list[str],
    ground_truth: str
) -> float:
    """
    Mean Reciprocal Rank.
    """

    scores = relevance_scores(

        retrieved_documents,

        ground_truth

    )

    for rank, score in enumerate(

        scores,

        start=1

    ):

        if score >= SIMILARITY_THRESHOLD:

            return 1 / rank

    return 0.0


def context_recall(
    retrieved_documents: list[str],
    ground_truth: str
) -> float:
    """
    Average semantic similarity
    between retrieved chunks
    and ground truth.
    """

    scores = relevance_scores(

        retrieved_documents,

        ground_truth

    )

    if not scores:

        return 0.0

    return sum(scores) / len(scores)