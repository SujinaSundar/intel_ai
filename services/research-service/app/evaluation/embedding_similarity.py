"""
Embedding similarity utilities.
"""

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def compute_similarity(
    text1: str,
    text2: str
) -> float:
    """
    Compute cosine similarity.

    Parameters
    ----------
    text1 : str

    text2 : str

    Returns
    -------
    float
    """

    embedding1 = embedding_model.encode(
        text1,
        convert_to_tensor=True
    )

    embedding2 = embedding_model.encode(
        text2,
        convert_to_tensor=True
    )

    similarity = cos_sim(
        embedding1,
        embedding2
    )

    return float(similarity)