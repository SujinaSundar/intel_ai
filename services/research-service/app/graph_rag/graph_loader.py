"""
Graph loader.

Loads report chunks and news,
extracts relationships,
and builds Neo4j graph.
"""

from app.database.connection import (
    SessionLocal
)

from app.database.models import (
    Company,
    ResearchReport,
    DocumentChunk,
    NewsMetadata
)

from app.graph_rag.relation_extractor import (
    extract_relations
)

from app.graph_rag.graph_builder import (
    create_node,
    create_relationship
)


ALLOWED_RELATIONS = {

    "HAS_CEO",

    "HAS_PRODUCT",

    "HAS_POLICY",

    "PARTNERS_WITH",

    "BELONGS_TO",

    "ACQUIRED",

    "INVESTS_IN",

    "SUBSIDIARY_OF",

    "FOCUSES_ON",

    "PROVIDES"
}


def load_company_chunks(
    company_name: str
) -> list[str]:
    """
    Load report chunks and news titles.
    """

    db = SessionLocal()

    try:

        company = (

            db.query(
                Company
            )

            .filter(
                Company.company_name ==
                company_name
            )

            .first()
        )

        if company is None:

            print(
                "Company not found."
            )

            return []

        print()

        print(
            "Company ID:",
            company.id
        )

        reports = (

            db.query(
                ResearchReport
            )

            .filter(
                ResearchReport.company_id ==
                company.id
            )

            .all()
        )

        print(
            "Reports:",
            len(reports)
        )

        report_chunks = (

            db.query(
                DocumentChunk.chunk_text
            )

            .join(
                ResearchReport,
                ResearchReport.id ==
                DocumentChunk.report_id
            )

            .filter(
                ResearchReport.company_id ==
                company.id
            )

            .all()
        )

        report_chunks = [

            row[0]

            for row in report_chunks
        ]

        print(
            "Report Chunks:",
            len(report_chunks)
        )

        news_titles = [

            row.title

            for row in

            db.query(
                NewsMetadata
            )

            .filter(
                NewsMetadata.company_id ==
                company.id
            )

            .all()

            if row.title
        ]

        print(
            "News Titles:",
            len(news_titles)
        )

        return (

            report_chunks

            +

            news_titles
        )

    finally:

        db.close()


def build_graph(
    company_name: str,
    max_chunks: int = 10
):
    """
    Build graph from company data.
    """

    chunks = load_company_chunks(
        company_name
    )

    print()

    print(
        f"Loaded {len(chunks)} chunks."
    )

    seen_relationships = set()

    total_triples = 0

    stored_triples = 0

    processed_chunks = 0

    for chunk in chunks[:max_chunks]:

        print()

        print(
            "-" * 80
        )

        print(
            f"Processing Chunk {processed_chunks + 1}"
        )

        triples = extract_relations(
            chunk
        )

        total_triples += len(
            triples
        )

        print(
            f"Triples Found: {len(triples)}"
        )

        for triple in triples:

            try:

                source = (
                    triple["source"]
                )

                source_type = (
                    triple["source_type"]
                )

                relation = (
                    triple["relation"]
                )

                target = (
                    triple["target"]
                )

                target_type = (
                    triple["target_type"]
                )
                GENERIC_ENTITIES = {

                    "partner",
                    "partners",

                    "customer",
                    "customers",

                    "employee",
                    "employees",

                    "stakeholder",
                    "stakeholders",

                    "company",
                    "organization",

                    "business",

                    "entity",

                    "group"
                }

                if target.lower() in GENERIC_ENTITIES:

                    continue

                # Normalize company entities

                if source_type in {

                    "Company",
                    "Organization",
                    "Bank"

                }:

                    source = company_name
                # Normalize generic entities

                if source_type == "Company":

                    source = company_name
                # Stage 2
                if relation not in ALLOWED_RELATIONS:

                    continue

                # Stage 3
                key = (

                    source,

                    relation,

                    target
                )

                if key in seen_relationships:

                    continue

                seen_relationships.add(
                    key
                )

                create_node(
                    source_type,
                    source
                )

                create_node(
                    target_type,
                    target
                )

                create_relationship(
                    source,
                    relation,
                    target
                )

                stored_triples += 1

                print()

                print(
                    source
                )

                print(
                    f"  └── {relation}"
                )

                print(
                    f"        └── {target}"
                )

            except Exception as error:

                print()

                print(
                    "Failed:"
                )

                print(
                    error
                )

        processed_chunks += 1

    print()

    print(
        "=" * 80
    )

    print(
        "GRAPH BUILD SUMMARY"
    )

    print(
        "=" * 80
    )

    print(
        f"Chunks Processed: {processed_chunks}"
    )

    print(
        f"Triples Extracted: {total_triples}"
    )

    print(
        f"Triples Stored: {stored_triples}"
    )

    print(
        f"Unique Relationships: {len(seen_relationships)}"
    )

    print(
        "=" * 80
    )
def build_graph_for_all_companies(
    max_chunks: int = 10
):
    """
    Build graph for all companies.
    """

    db = SessionLocal()

    try:

        companies = (

            db.query(
                Company
            )

            .all()
        )

        print()

        print(
            f"Found {len(companies)} companies."
        )

        for company in companies:

            print()

            print(
                "=" * 80
            )

            print(
                f"Building Graph For: "
                f"{company.company_name}"
            )

            print(
                "=" * 80
            )

            build_graph(

                company_name=
                company.company_name,

                max_chunks=
                max_chunks
            )

    finally:

        db.close()

if __name__ == "__main__":

    build_graph_for_all_companies(
        max_chunks=5
    )