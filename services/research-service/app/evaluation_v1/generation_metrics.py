"""
Generation evaluation metrics.
"""

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

# Load once
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def semantic_similarity(
    generated_answer: str,
    ground_truth: str
) -> float:
    """
    Compute semantic similarity between
    generated answer and ground truth.

    Returns
    -------
    float
        Cosine similarity.
    """

    generated_embedding = embedding_model.encode(
        generated_answer,
        convert_to_tensor=True
    )

    ground_truth_embedding = embedding_model.encode(
        ground_truth,
        convert_to_tensor=True
    )

    similarity = cos_sim(
        generated_embedding,
        ground_truth_embedding
    )

    return float(similarity)


def answer_correctness(
    generated_answer: str,
    ground_truth: str,
    threshold: float = 0.80
) -> float:
    """
    Binary correctness score.

    Parameters
    ----------
    threshold : float

    Returns
    -------
    float
    """

    score = semantic_similarity(
        generated_answer,
        ground_truth
    )

    if score >= threshold:

        return 1.0

    return 0.0