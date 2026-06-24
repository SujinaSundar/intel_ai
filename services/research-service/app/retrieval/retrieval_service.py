"""
Retrieval service.

Workflow
--------
Question
    ↓
Generate Query Embedding
    ↓
ChromaDB Search
    ↓
Top K Chunks
"""

from app.embeddings.embedding_service import (
    generate_embedding
)

from app.vector_store.chroma_service import (
    collection
)


def retrieve_documents(
    query: str,
    top_k: int = 5
) -> list[str]:
    """
    Retrieve relevant chunks from ChromaDB.

    Parameters
    ----------
    query : str
        User question.

    top_k : int
        Number of chunks to retrieve.

    Returns
    -------
    list[str]
    """

    query_embedding = generate_embedding(
        query
    )

    results = collection.query(

        query_embeddings=[
            query_embedding
        ],

        n_results=top_k
    )

    documents = results["documents"][0]

    unique_documents = []

    for document in documents:

        if document not in unique_documents:

            unique_documents.append(
                document
            )

    print(
        f"Retrieved {len(documents)} chunks."
    )

    print(
        f"Unique chunks: {len(unique_documents)}"
    )

    return unique_documents