"""
Retrieval Service.

Workflow
--------
Question
    ↓
Generate Query Embedding
    ↓
ChromaDB Search
        ↓
(Optional Company Filter)
        ↓
Top K Chunks
"""

import logging
import time

from app.embeddings.embedding_service import (
    generate_embedding,
)
from app.exceptions.custom_exceptions import (
    ExternalAPIException,
    InvalidRequestException,
)
from app.vector_store.chroma_service import (
    collection,
)

logger = logging.getLogger(__name__)


def retrieve_documents(
    query: str,
    company_name: str | None = None,
    top_k: int = 5,
) -> dict:
    """
    Retrieve relevant chunks from ChromaDB.

    Parameters
    ----------
    query : str
        User question.

    company_name : str | None
        Optional company filter.

    top_k : int
        Number of chunks to retrieve.

    Returns
    -------
    dict
        Retrieved documents and metadata.
    """

    if not query.strip():
        raise InvalidRequestException(
            "Query cannot be empty."
        )

    logger.info("Generating query embedding.")

    start_time = time.perf_counter()

    try:

        query_embedding = generate_embedding(
            query
        )

        logger.info("Query embedding generated.")

        # -----------------------------------
        # Company-specific retrieval
        # -----------------------------------

        if company_name:

            logger.info(
                "Searching ChromaDB for company: %s",
                company_name,
            )

            results = collection.query(
                query_embeddings=[
                    query_embedding
                ],
                where={
                    "company_name": company_name
                },
                n_results=top_k,
            )

        # -----------------------------------
        # Global retrieval
        # -----------------------------------

        else:

            logger.info(
                "Performing global vector retrieval."
            )

            results = collection.query(
                query_embeddings=[
                    query_embedding
                ],
                n_results=top_k,
            )

    except Exception as error:

        logger.exception(
            "Vector retrieval failed."
        )

        raise ExternalAPIException(
            f"Vector retrieval failed: {error}"
        ) from error

    retrieval_time = (
        time.perf_counter() - start_time
    )

    documents = (
        results.get("documents", [[]])[0]
        if results.get("documents")
        else []
    )

    metadata = (
        results.get("metadatas", [[]])[0]
        if results.get("metadatas")
        else []
    )

    unique_documents = []

    for document in documents:

        if document not in unique_documents:

            unique_documents.append(
                document
            )

    logger.info(
        "Retrieved %d chunks (%d unique) in %.3f seconds.",
        len(documents),
        len(unique_documents),
        retrieval_time,
    )

    return {
        "documents": unique_documents,
        "metadata": metadata,
    }