"""
Graph Loader.

Loads annual report chunks,
extracts relationships,
and builds the Neo4j graph.
"""

import logging
from datetime import datetime, timezone

from app.database.connection import SessionLocal
from app.database.models import (
    Company,
    DocumentChunk,
    ResearchReport,
)
from app.exceptions.custom_exceptions import (
    CompanyNotFoundException,
    DatabaseException,
)
from app.graph_rag.graph_builder import (
    create_node,
    create_relationship,
)
from app.graph_rag.relation_extractor import (
    extract_relations,
)
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# Allowed Relationships
# ---------------------------------------------------------

ALLOWED_RELATIONS = {
    "HAS_CEO",
    "HAS_CFO",
    "HAS_CHAIRMAN",
    "HAS_MANAGING_DIRECTOR",
    "HAS_FOUNDER",
    "HAS_PRODUCT",
    "HAS_SERVICE",
    "HAS_PLATFORM",
    "HAS_TECHNOLOGY",
    "PROVIDES",
    "OFFERS",
    "FOCUSES_ON",
    "OPERATES_IN",
    "SERVES",
    "EXPANDS_TO",
    "PARTNERS_WITH",
    "ACQUIRED",
    "SUBSIDIARY_OF",
    "INVESTS_IN",
    "BELONGS_TO",
    "DEVELOPS",
    "USES",
    "LAUNCHED",
    "HAS_REVENUE",
    "HAS_NET_PROFIT",
    "HAS_OPERATING_PROFIT",
    "HAS_EPS",
    "HAS_ROE",
    "HAS_ROA",
    "HAS_MARKET_CAP",
    "HAS_PE_RATIO",
    "HAS_PB_RATIO",
    "HAS_DIVIDEND",
    "HAS_GROSS_NPA",
    "HAS_NET_NPA",
    "HAS_CASA_RATIO",
    "SUPPORTS",
    "PROMOTES",
    "REDUCES_EMISSIONS",
}

# ---------------------------------------------------------
# Generic Entities
# ---------------------------------------------------------

GENERIC_ENTITIES = {
    "company",
    "companies",
    "organization",
    "organisations",
    "business",
    "entity",
    "group",
    "partner",
    "partners",
    "customer",
    "customers",
    "client",
    "clients",
    "employee",
    "employees",
    "stakeholder",
    "stakeholders",
    "service",
    "services",
    "product",
    "products",
    "technology",
    "platform",
    "solution",
    "initiative",
    "market",
    "markets",
    "industry",
    "industries",
}


# ---------------------------------------------------------
# Load Company Chunks
# ---------------------------------------------------------

def load_company_chunks(
    db,
    company_name: str,
):
    """
    Load all chunks belonging to
    a company's research reports.
    """

    logger.info(
        "Loading document chunks for company: %s",
        company_name,
    )

    company = (
        db.query(Company)
        .filter(
            Company.company_name == company_name
        )
        .first()
    )

    if company is None:

        logger.warning(
            "Company not found: %s",
            company_name,
        )

        raise CompanyNotFoundException(
            company_name
        )

    chunks = (
        db.query(DocumentChunk)
        .join(
            ResearchReport,
            ResearchReport.id == DocumentChunk.report_id,
        )
        .filter(
            ResearchReport.company_id == company.id
        )
        .all()
    )

    logger.info(
        "Loaded %d chunks.",
        len(chunks),
    )

    return chunks


# ---------------------------------------------------------
# Build Graph
# ---------------------------------------------------------

def build_graph(
    db,
    company_name: str,
    max_chunks: int = 50,
) -> bool:
    """
    Build Neo4j graph for a company.

    Parameters
    ----------
    db
        Active database session.

    company_name : str
        Company name.

    max_chunks : int
        Maximum number of chunks
        processed.

    Returns
    -------
    bool
        True if successful.
    """

    logger.info(
        "Building graph for company: %s",
        company_name,
    )

    chunks = load_company_chunks(
        db=db,
        company_name=company_name,
    )

    if not chunks:

        logger.warning(
            "No chunks found for company: %s",
            company_name,
        )

        return False

    seen = set()

    try:

        for chunk in chunks[:max_chunks]:

            triples = extract_relations(
                company_name=company_name,
                text=chunk.chunk_text,
            )

            logger.info(
                "Extracted %d relations.",
                len(triples),
            )

            for triple in triples:

                source = triple["source"].strip()
                source_type = (
                    triple["source_type"].strip()
                )

                relation = (
                    triple["relation"]
                    .strip()
                    .upper()
                )

                target = triple["target"].strip()
                target_type = (
                    triple["target_type"].strip()
                )

                # ---------------------------------
                # Validation
                # ---------------------------------

                if (
                    source.lower()
                    != company_name.lower()
                ):
                    continue

                source = company_name

                if (
                    target.lower()
                    in GENERIC_ENTITIES
                ):
                    continue

                if len(target) < 3:
                    continue

                if (
                    target.lower()
                    == company_name.lower()
                ):
                    continue

                if (
                    relation
                    not in ALLOWED_RELATIONS
                ):
                    continue

                if source_type in {
                    "Company",
                    "Organization",
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
                    "Industry",
                }:
                    target = target.title()

                key = (
                    source.lower(),
                    relation,
                    target.lower(),
                )

                if key in seen:
                    continue

                seen.add(key)

                create_node(
                    source_type,
                    source,
                )

                create_node(
                    target_type,
                    target,
                )

                create_relationship(
                    source,
                    relation,
                    target,
                )

                logger.info(
                    "%s --%s--> %s",
                    source,
                    relation,
                    target,
                )

        logger.info(
            "Graph built successfully for %s.",
            company_name,
        )

        return True

    except SQLAlchemyError as error:

        logger.exception(
            "Database error while building graph."
        )

        raise DatabaseException(
            str(error)
        ) from error

    except Exception:

        logger.exception(
            "Unexpected error while building graph."
        )

        raise
# ---------------------------------------------------------
# Build Graph for All Companies
# ---------------------------------------------------------

def build_graph_for_all_companies(
    max_chunks: int = 50,
) -> None:
    """
    Build Neo4j graphs for all
    pending or failed reports.

    Parameters
    ----------
    max_chunks : int
        Maximum chunks processed
        per company.
    """

    logger.info(
        "Starting graph build for all companies."
    )

    db = SessionLocal()

    try:

        # -------------------------------------------------
        # Recover Interrupted Jobs
        # -------------------------------------------------

        interrupted = (
            db.query(ResearchReport)
            .filter(
                ResearchReport.graph_status
                == "PROCESSING"
            )
            .all()
        )

        for report in interrupted:
            report.graph_status = "FAILED"

        if interrupted:

            db.commit()

            logger.warning(
                "Recovered %d interrupted graph build(s).",
                len(interrupted),
            )

        # -------------------------------------------------
        # Fetch Pending Reports
        # -------------------------------------------------

        reports = (
            db.query(
                ResearchReport,
                Company,
            )
            .join(
                Company,
                Company.id
                == ResearchReport.company_id,
            )
            .filter(
                ResearchReport.graph_status.in_(
                    [
                        "PENDING",
                        "FAILED",
                    ]
                )
            )
            .all()
        )

        if not reports:

            logger.info(
                "No pending graph builds found."
            )

            return

        logger.info(
            "Found %d reports to process.",
            len(reports),
        )

        # -------------------------------------------------
        # Process Reports
        # -------------------------------------------------

        for report, company in reports:

            logger.info("=" * 80)
            logger.info(
                "Processing company: %s",
                company.company_name,
            )
            logger.info(
                "Current status: %s",
                report.graph_status,
            )
            logger.info("=" * 80)

            report.graph_status = "PROCESSING"
            db.commit()

            try:

                success = build_graph(
                    db=db,
                    company_name=company.company_name,
                    max_chunks=max_chunks,
                )

                if success:

                    report.graph_status = "COMPLETED"
                    report.graph_processed_at = (
                        datetime.now(timezone.utc)
                    )

                    db.commit()

                    logger.info(
                        "Graph build completed for %s.",
                        company.company_name,
                    )

                else:

                    report.graph_status = "FAILED"

                    db.commit()

                    logger.warning(
                        "Graph build failed for %s.",
                        company.company_name,
                    )

            except Exception:

                report.graph_status = "FAILED"

                db.commit()

                logger.exception(
                    "Unexpected failure while processing %s.",
                    company.company_name,
                )

        logger.info(
            "Completed graph build workflow."
        )

    except SQLAlchemyError as error:

        logger.exception(
            "Database error during graph build workflow."
        )

        raise DatabaseException(
            str(error)
        ) from error

    finally:

        db.close()

        logger.info(
            "Database session closed."
        )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    logger.info(
        "Starting Graph Loader."
    )

    build_graph_for_all_companies(
        max_chunks=50,
    )

    logger.info(
        "Graph Loader finished."
    )