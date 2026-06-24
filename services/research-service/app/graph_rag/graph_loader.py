"""
Graph loader.

Workflow
--------
Reports
+
News
    ↓
Chunks
    ↓
Relation Extractor
    ↓
Triples
    ↓
Graph Builder
    ↓
Neo4j
"""

from app.database.connection import (
    SessionLocal
)

from app.database.models import (
    DocumentChunk,
    NewsMetadata
)


def load_chunks() -> list[str]:
    """
    Load report chunks and news content.

    Returns
    -------
    list[str]
    """

    db = SessionLocal()

    try:

        report_chunks = [

            row.chunk_text

            for row in

            db.query(
                DocumentChunk
            ).all()

        ]

        news_chunks = [

            row.title

            for row in

            db.query(
                NewsMetadata
            ).all()

            if row.title
        ]

        all_chunks = (

            report_chunks

            +

            news_chunks
        )

        return all_chunks

    finally:

        db.close()


def build_graph():
    """
    Build graph.

    To be implemented later.

    Workflow
    --------
    Chunks
        ↓
    Relation Extractor
        ↓
    Graph Builder
        ↓
    Neo4j
    """

    chunks = load_chunks()

    print()

    print(
        f"Loaded {len(chunks)} chunks."
    )

    # Later:
    #
    # for chunk in chunks:
    #
    #     triples = extract_relations(
    #         chunk
    #     )
    #
    #     for triple in triples:
    #
    #         create_node()
    #
    #         create_relationship()


if __name__ == "__main__":

    build_graph()