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

import logging

from app.database.connection import SessionLocal
from app.database.models import (
    Company,
    DocumentChunk,
    ResearchReport,
)
from app.embeddings.embedding_model import (
    embedding_model,
)
from app.exceptions.custom_exceptions import (
    DatabaseException,
    ExternalAPIException,
)
from app.vector_store.chroma_service import (
    collection,
)
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


def generate_embeddings() -> None:
    """
    Generate embeddings for report chunks and
    store them in ChromaDB.
    """

    db = SessionLocal()

    try:

        logger.info(
            "Fetching non-embedded document chunks."
        )

        rows = (
            db.query(
                DocumentChunk,
                ResearchReport,
                Company,
            )
            .join(
                ResearchReport,
                DocumentChunk.report_id == ResearchReport.id,
            )
            .join(
                Company,
                ResearchReport.company_id == Company.id,
            )
            .filter(
                DocumentChunk.is_embedded.is_(False)
            )
            .all()
        )

        if not rows:

            logger.info(
                "No document chunks found for embedding."
            )

            return

        logger.info(
            "Found %d document chunks.",
            len(rows),
        )

        texts = [
            chunk.chunk_text
            for chunk, _, _ in rows
        ]

        logger.info(
            "Generating embeddings."
        )

        try:

            embeddings = embedding_model.encode(
                texts,
                batch_size=32,
                show_progress_bar=True,
            )

        except Exception as error:

            logger.exception(
                "Embedding generation failed."
            )

            raise ExternalAPIException(
                f"Embedding generation failed: {error}"
            ) from error

        batch_size = 5000

        logger.info(
            "Storing embeddings in ChromaDB."
        )

        for i in range(
            0,
            len(rows),
            batch_size,
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
                        "chunk_number": chunk.chunk_number,
                    }
                    for chunk, report, company in batch_rows
                ],
            )

            logger.info(
                "Inserted %d/%d chunks.",
                min(
                    i + batch_size,
                    len(rows),
                ),
                len(rows),
            )

        logger.info(
            "Updating PostgreSQL embedding status."
        )

        for chunk, _, _ in rows:

            chunk.is_embedded = True

        db.commit()

        logger.info(
            "Embedding generation completed successfully."
        )

    except SQLAlchemyError as error:

        db.rollback()

        logger.exception(
            "Database error during embedding generation."
        )

        raise DatabaseException(
            f"Embedding generation database error: {error}"
        ) from error

    finally:

        db.close()

        logger.info(
            "Database session closed."
        )


if __name__ == "__main__":

    generate_embeddings()