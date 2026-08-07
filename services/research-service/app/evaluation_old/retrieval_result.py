"""
Common retrieval result.
"""

from dataclasses import dataclass


@dataclass
class RetrievalResult:
    """
    Standard output returned by every retrieval pipeline.
    """

    pipeline: str

    answer: str

    documents: list[str]

    graph_context: list[str]

    sentiment: dict | None

    stock: dict | None

    retrieval_time: float

    num_chunks: int