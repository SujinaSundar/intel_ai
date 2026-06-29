"""
Common retrieval result.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class RetrievalResult:
    """
    Standard output returned by every retrieval pipeline.
    """

    pipeline: str

    answer: str

    documents: list[str]

    graph_context: list[str]

    sentiment: Optional[dict]

    stock: Optional[dict]

    retrieval_time: float

    num_chunks: int