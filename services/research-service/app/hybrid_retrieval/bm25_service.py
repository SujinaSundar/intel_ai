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
    DocumentChunk,
    ResearchReport,
    Company
)


def bm25_retrieve(
    query: str,
    company_name: str | None = None,
    top_k: int = 5
) -> dict:
    """
    Retrieve relevant chunks using BM25.

    Parameters
    ----------
    query : str

    company_name : str | None
        Optional company filter.

    top_k : int

    Returns
    -------
    dict
    """

    db = SessionLocal()

    try:

        rows = (

            db.query(
                DocumentChunk,
                ResearchReport,
                Company
            )

            .join(
                ResearchReport,
                DocumentChunk.report_id == ResearchReport.id
            )

            .join(
                Company,
                ResearchReport.company_id == Company.id
            )

        )

        # -----------------------------
        # Optional company filter
        # -----------------------------

        if company_name:

            rows = rows.filter(
                Company.company_name.ilike(
                    company_name
                )
            )

        rows = rows.all()

        if not rows:

            return {

                "documents": [],

                "metadata": []

            }

        documents = [

            chunk.chunk_text

            for chunk, _, _ in rows

        ]

        tokenized_corpus = [

            document.lower().split()

            for document in documents

        ]

        bm25 = BM25Okapi(
            tokenized_corpus
        )

        tokenized_query = (
            query.lower().split()
        )

        scores = bm25.get_scores(
            tokenized_query
        )

        ranked_indices = sorted(

            range(len(scores)),

            key=lambda i: scores[i],

            reverse=True

        )[:top_k]

        retrieved_documents = []

        metadata = []

        for index in ranked_indices:

            chunk, report, company = rows[index]

            retrieved_documents.append(
                chunk.chunk_text
            )

            metadata.append(

                {

                    "document": chunk.chunk_text,

                    "company_id": company.id,

                    "company_name": company.company_name,

                    "report_id": report.id,

                    "report_type": report.report_type,

                    "year": report.year,

                    "chunk_number": chunk.chunk_number

                }

            )

        return {

            "documents": retrieved_documents,

            "metadata": metadata

        }

    finally:

        db.close()