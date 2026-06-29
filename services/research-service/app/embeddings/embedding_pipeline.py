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
    DocumentChunk,
    ResearchReport,
    Company
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

            .filter(
                DocumentChunk.is_embedded == False
            )

            .all()

        )

        if not rows:

            print(
                "No chunks found."
            )

            return

        print(
            f"Found {len(rows)} chunks."
        )

        texts = [

            chunk.chunk_text

            for chunk, report, company in rows

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

            len(rows),

            batch_size

        ):

            batch_rows = rows[
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

                    for chunk, _, _ in batch_rows

                ],

                embeddings=batch_embeddings.tolist(),

                documents=batch_texts,

                metadatas=[

                    {

                        "company_id": company.id,

                        "company_name": company.company_name,

                        "report_id": report.id,

                        "report_type": report.report_type,

                        "year": report.year,

                        "chunk_number": chunk.chunk_number

                    }

                    for chunk, report, company in batch_rows

                ]

            )

            print(

                f"Inserted "

                f"{min(i + batch_size, len(rows))}"

                f"/{len(rows)} chunks"

            )

        print(
            "Updating PostgreSQL..."
        )

        for chunk, _, _ in rows:

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