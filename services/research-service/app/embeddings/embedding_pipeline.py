"""
Embedding generation pipeline.

Workflow
--------
Document Chunks
       ↓
Generate Embeddings
       ↓
Store in ChromaDB
       ↓
Mark as Embedded
"""

from app.database.connection import SessionLocal

from app.database.models import (
    DocumentChunk
)

from app.embeddings.embedding_model import (
    embedding_model
)

from app.vector_store.chroma_service import (
    collection
)


def generate_embeddings() -> None:
    """
    Generate embeddings for report chunks and
    store them in ChromaDB.

    Steps
    -----
    1. Fetch chunks that are not embedded.
    2. Generate embeddings using SentenceTransformer.
    3. Store embeddings in ChromaDB.
    4. Mark chunks as embedded.

    Returns
    -------
    None
    """

    db = SessionLocal()

    try:

        chunks = (
            db.query(DocumentChunk)
            .filter(
                DocumentChunk.is_embedded == False
            )
            .all()
        )

        if not chunks:

            print(
                "No chunks found."
            )

            return

        print(
            f"Found {len(chunks)} chunks."
        )

        # Extract chunk texts
        texts = [
            chunk.chunk_text
            for chunk in chunks
        ]

        print(
            "Generating embeddings..."
        )

        embeddings = embedding_model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True
        )

        batch_size = 5000

        print(
            "Storing embeddings in ChromaDB..."
        )

        for i in range(
            0,
            len(chunks),
            batch_size
        ):

            batch_chunks = chunks[
                i:i + batch_size
            ]

            batch_embeddings = embeddings[
                i:i + batch_size
            ]

            batch_texts = texts[
                i:i + batch_size
            ]

            collection.add(

                ids=[
                    str(chunk.id)
                    for chunk in batch_chunks
                ],

                embeddings=batch_embeddings.tolist(),

                documents=batch_texts,

                metadatas=[

                    {
                        "report_id": chunk.report_id,
                        "chunk_number": chunk.chunk_number
                    }

                    for chunk in batch_chunks

                ]
            )

            print(
                f"Inserted "
                f"{min(i + batch_size, len(chunks))}"
                f"/{len(chunks)} chunks"
            )

        print(
            "Updating PostgreSQL..."
        )

        for chunk in chunks:

            chunk.is_embedded = True

        db.commit()

        print(
            "Embedding generation completed successfully."
        )

    except Exception as error:

        db.rollback()

        print(
            f"Error generating embeddings: {error}"
        )

    finally:

        db.close()


if __name__ == "__main__":

    generate_embeddings()