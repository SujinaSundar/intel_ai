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
(Optional Company Filter)
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
    company_name: str | None = None,
    top_k: int = 5
) -> list[str]:
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
    list[str]
    """

    query_embedding = generate_embedding(
        query
    )

    # -----------------------------------
    # Company-specific retrieval
    # -----------------------------------

    if company_name:

        print(
            f"Retrieving documents for: {company_name}"
        )

        results = collection.query(

            query_embeddings=[
                query_embedding
            ],

            where={
                "company_name": company_name
            },

            n_results=top_k

        )

    # -----------------------------------
    # Global retrieval
    # -----------------------------------

    else:

        print(
            "Performing global retrieval..."
        )

        results = collection.query(

            query_embeddings=[
                query_embedding
            ],

            n_results=top_k

        )

    documents = []

    if results["documents"]:

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

    return {
        
    "documents": unique_documents,
    "metadata": results["metadatas"][0]
}
    