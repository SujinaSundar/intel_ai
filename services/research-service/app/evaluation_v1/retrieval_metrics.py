"""
Retrieval evaluation metrics.
"""



def hit_rate(
    retrieved_documents: list[str],
    ground_truth: str
) -> float:
    """
    Returns 1 if any retrieved chunk contains
    the ground truth answer.
    """

    ground_truth = ground_truth.lower()

    for document in retrieved_documents:

        if ground_truth in document.lower():

            return 1.0

    return 0.0


def precision_at_k(
    retrieved_documents: list[str],
    ground_truth: str
) -> float:
    """
    Precision@k
    """

    if not retrieved_documents:

        return 0.0

    relevant = 0

    ground_truth = ground_truth.lower()

    for document in retrieved_documents:

        if ground_truth in document.lower():

            relevant += 1

    return relevant / len(retrieved_documents)


def recall_at_k(
    retrieved_documents: list[str],
    ground_truth: str
) -> float:
    """
    Recall@k
    """

    ground_truth = ground_truth.lower()

    for document in retrieved_documents:

        if ground_truth in document.lower():

            return 1.0

    return 0.0


def mean_reciprocal_rank(
    retrieved_documents: list[str],
    ground_truth: str
) -> float:
    """
    MRR
    """

    ground_truth = ground_truth.lower()

    for rank, document in enumerate(
        retrieved_documents,
        start=1
    ):

        if ground_truth in document.lower():

            return 1 / rank

    return 0.0


def context_recall(
    retrieved_documents: list[str],
    ground_truth: str
) -> float:
    """
    Context Recall
    """

    return recall_at_k(
        retrieved_documents,
        ground_truth
    )