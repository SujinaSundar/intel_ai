"""
Graph loader.

Loads annual report chunks,
extracts relationships,
and builds Neo4j graph.
"""

from datetime import datetime

from app.database.connection import SessionLocal
from app.database.models import (
    Company,
    ResearchReport,
    DocumentChunk,
)
from app.graph_rag.relation_extractor import extract_relations
from app.graph_rag.graph_builder import (
    create_node,
    create_relationship,
)

ALLOWED_RELATIONS = {
    "HAS_CEO","HAS_CFO","HAS_CHAIRMAN","HAS_MANAGING_DIRECTOR","HAS_FOUNDER",
    "HAS_PRODUCT","HAS_SERVICE","HAS_PLATFORM","HAS_TECHNOLOGY",
    "PROVIDES","OFFERS",
    "FOCUSES_ON","OPERATES_IN","SERVES","EXPANDS_TO",
    "PARTNERS_WITH","ACQUIRED","SUBSIDIARY_OF","INVESTS_IN","BELONGS_TO",
    "DEVELOPS","USES","LAUNCHED",
    "HAS_REVENUE","HAS_NET_PROFIT","HAS_OPERATING_PROFIT","HAS_EPS",
    "HAS_ROE","HAS_ROA","HAS_MARKET_CAP","HAS_PE_RATIO","HAS_PB_RATIO",
    "HAS_DIVIDEND","HAS_GROSS_NPA","HAS_NET_NPA","HAS_CASA_RATIO",
    "SUPPORTS","PROMOTES","REDUCES_EMISSIONS"
}

GENERIC_ENTITIES = {
    "company","companies","organization","organisations",
    "business","entity","group",
    "partner","partners",
    "customer","customers",
    "client","clients",
    "employee","employees",
    "stakeholder","stakeholders",
    "service","services",
    "product","products",
    "technology","platform",
    "solution","initiative",
    "market","markets",
    "industry","industries"
}


def load_company_chunks(
    db,
    company_name: str
):
    """
    Load all chunks belonging to a company's reports.
    Uses the existing database session.
    """

    company = (
        db.query(Company)
        .filter(
            Company.company_name == company_name
        )
        .first()
    )

    if company is None:
        print(f"{company_name} not found.")
        return []

    chunks = (
        db.query(DocumentChunk)
        .join(
            ResearchReport,
            ResearchReport.id == DocumentChunk.report_id
        )
        .filter(
            ResearchReport.company_id == company.id
        )
        .all()
    )

    return chunks
def build_graph(
    db,
    company_name: str,
    max_chunks: int = 50
) -> bool:
    """
    Build Neo4j graph for a single company.
    Returns True if successful, False otherwise.
    """

    chunks = load_company_chunks(
        db=db,
        company_name=company_name
    )

    if not chunks:
        print(f"No chunks found for {company_name}")
        return False

    seen = set()

    try:

        for chunk in chunks[:max_chunks]:

            triples = extract_relations(
                company_name=company_name,
                text=chunk.chunk_text
            )

            for triple in triples:

                source = triple["source"].strip()
                source_type = triple["source_type"].strip()

                relation = (
                    triple["relation"]
                    .strip()
                    .upper()
                )

                target = triple["target"].strip()
                target_type = triple["target_type"].strip()

                if source.lower() != company_name.lower():
                    continue

                source = company_name

                if target.lower() in GENERIC_ENTITIES:
                    continue

                if len(target) < 3:
                    continue

                if target.lower() == company_name.lower():
                    continue

                if relation not in ALLOWED_RELATIONS:
                    continue

                if source_type in {
                    "Company",
                    "Organization"
                }:
                    source = company_name

                if target_type in {
                    "Product",
                    "Service",
                    "Technology",
                    "Platform",
                    "Initiative",
                    "Policy",
                    "Sector",
                    "Industry"
                }:
                    target = target.title()

                key = (
                    source.lower(),
                    relation,
                    target.lower()
                )

                if key in seen:
                    continue

                seen.add(key)

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

                print(
                    f"{source} --{relation}--> {target}"
                )

        return True

    except Exception as e:

        print(
            f"Error building graph for {company_name}: {e}"
        )

        return False
def build_graph_for_all_companies(
    max_chunks: int = 50
):
    """
    Build graphs for all pending or failed reports.
    """

    db = SessionLocal()

    try:

        # ------------------------------------------------------------------
        # Recover interrupted graph builds
        # ------------------------------------------------------------------
        interrupted = (
            db.query(ResearchReport)
            .filter(
                ResearchReport.graph_status == "PROCESSING"
            )
            .all()
        )

        for report in interrupted:
            report.graph_status = "FAILED"

        if interrupted:
            db.commit()
            print(
                f"Recovered {len(interrupted)} interrupted graph build(s)."
            )

        # ------------------------------------------------------------------
        # Fetch reports to process
        # ------------------------------------------------------------------
        reports = (
            db.query(
                ResearchReport,
                Company
            )
            .join(
                Company,
                Company.id == ResearchReport.company_id
            )
            .filter(
                ResearchReport.graph_status.in_(
                    [
                        "PENDING",
                        "FAILED"
                    ]
                )
            )
            .all()
        )

        if not reports:

            print("No pending reports found.")
            return

        for report, company in reports:

            print("=" * 80)
            print(f"Processing : {company.company_name}")
            print(f"Current Status : {report.graph_status}")
            print("=" * 80)

            report.graph_status = "PROCESSING"
            db.commit()

            success = build_graph(
                db=db,
                company_name=company.company_name,
                max_chunks=max_chunks
            )

            if success:

                report.graph_status = "COMPLETED"
                report.graph_processed_at = datetime.utcnow()
                db.commit()

                print(f"✅ {company.company_name} completed.")

            else:

                report.graph_status = "FAILED"
                db.commit()

                print(f"❌ {company.company_name} failed.")

    finally:

        db.close()


"""if __name__ == "__main__":
   build_graph(
    company_name="HDFC Bank",
    max_chunks=10
)"""
if __name__ == "__main__":
    build_graph_for_all_companies(max_chunks=50)
