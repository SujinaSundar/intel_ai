"""
Reciprocal Rank Fusion.
"""


def reciprocal_rank_fusion(
    vector_results: list[str],
    bm25_results: list[str],
    k: int = 60
) -> list[str]:
    """
    Combine vector and BM25 results.

    Parameters
    ----------
    vector_results : list[str]

    bm25_results : list[str]

    k : int

    Returns
    -------
    list[str]
    """

    scores = {}

    for rank, document in enumerate(
        vector_results,
        start=1
    ):

        scores[document] = (
            scores.get(document, 0)
            + 1 / (k + rank)
        )

    for rank, document in enumerate(
        bm25_results,
        start=1
    ):

        scores[document] = (
            scores.get(document, 0)
            + 1 / (k + rank)
        )

    ranked_documents = sorted(

        scores,

        key=scores.get,

        reverse=True
    )

    return ranked_documents