"""
Generation evaluation metrics.
"""

from app.evaluation.embedding_similarity import (
    compute_similarity
)


def semantic_similarity(
    generated_answer: str,
    ground_truth: str
) -> float:
    """
    Compute semantic similarity between
    generated answer and ground truth.

    Parameters
    ----------
    generated_answer : str

    ground_truth : str

    Returns
    -------
    float
    """

    return compute_similarity(

        generated_answer,

        ground_truth

    )


def answer_correctness(
    generated_answer: str,
    ground_truth: str,
    threshold: float = 0.80
) -> float:
    """
    Binary answer correctness.

    Parameters
    ----------
    generated_answer : str

    ground_truth : str

    threshold : float

    Returns
    -------
    float
    """

    similarity = semantic_similarity(

        generated_answer,

        ground_truth

    )

    if similarity >= threshold:

        return 1.0

    return 0.0