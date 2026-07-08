"""
Graph loader.

Loads annual report chunks,
extracts relationships,
and builds Neo4j graph.
"""

from app.database.connection import SessionLocal
from app.database.models import Company, ResearchReport, DocumentChunk
from app.graph_rag.relation_extractor import extract_relations
from app.graph_rag.graph_builder import create_node, create_relationship

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


def load_company_chunks(company_name: str) -> list[str]:

    db = SessionLocal()

    try:
        company = (
            db.query(Company)
            .filter(Company.company_name == company_name)
            .first()
        )

        if company is None:
            print("Company not found.")
            return []

        rows = (
            db.query(DocumentChunk.chunk_text)
            .join(
                ResearchReport,
                ResearchReport.id == DocumentChunk.report_id
            )
            .filter(
                ResearchReport.company_id == company.id
            )
            .all()
        )

        return [r[0] for r in rows]

    finally:
        db.close()


def build_graph(
    company_name: str,
    max_chunks: int = 50
):

    chunks = load_company_chunks(company_name)

    seen = set()

    for chunk in chunks[:max_chunks]:

        triples = extract_relations(
            company_name=company_name,
            text=chunk
        )

        for triple in triples:

            try:

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

                create_node(source_type, source)
                create_node(target_type, target)
                create_relationship(source, relation, target)

                print(f"{source} --{relation}--> {target}")

            except Exception as e:
                print("Failed:", e)


def build_graph_for_all_companies(max_chunks: int = 50):

    db = SessionLocal()

    try:
        companies = db.query(Company).all()

        for company in companies:

            print("=" * 80)
            print(company.company_name)
            print("=" * 80)

            build_graph(
                company.company_name,
                max_chunks=max_chunks
            )

    finally:
        db.close()


if __name__ == "__main__":
   build_graph(
    company_name="HDFC Bank",
    max_chunks=10
)

