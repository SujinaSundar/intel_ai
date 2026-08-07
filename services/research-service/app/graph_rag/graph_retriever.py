"""
Graph Retrieval Service.

Workflow
--------
Question
    ↓
Detect Relevant Relations
    ↓
Neo4j Retrieval
    ↓
Graph Context
"""

import logging

from app.exceptions.custom_exceptions import (
    DatabaseException,
    InvalidRequestException,
)
from app.graph_rag.neo4j_service import (
    get_driver,
)
from neo4j.exceptions import Neo4jError

logger = logging.getLogger(__name__)


def detect_relations(
    question: str,
) -> list[str]:
    """
    Detect relevant relationship types
    from the user question.
    """

    question = question.lower()

    relation_map = {
        "HAS_PRODUCT": [
            "product",
            "loan",
            "card",
            "insurance",
            "service",
        ],
        "PROVIDES": [
            "provide",
            "provides",
            "offer",
            "offers",
            "service",
        ],
        "FOCUSES_ON": [
            "focus",
            "strategy",
            "initiative",
            "priority",
        ],
        "HAS_CEO": [
            "ceo",
            "chief executive",
        ],
        "HAS_CFO": [
            "cfo",
            "finance officer",
        ],
        "HAS_CHAIRMAN": [
            "chairman",
            "chairperson",
        ],
        "ACQUIRED": [
            "acquired",
            "acquisition",
            "merged",
            "merger",
            "bought",
        ],
        "PARTNERS_WITH": [
            "partner",
            "partnership",
            "collaboration",
        ],
        "INVESTS_IN": [
            "invest",
            "investment",
        ],
        "HAS_REVENUE": [
            "revenue",
            "sales",
        ],
        "HAS_NET_PROFIT": [
            "profit",
            "net profit",
            "earnings",
        ],
        "HAS_OPERATING_PROFIT": [
            "operating profit",
            "ebit",
        ],
        "HAS_EPS": [
            "eps",
            "earnings per share",
        ],
        "HAS_ROE": [
            "roe",
            "return on equity",
        ],
        "HAS_ROA": [
            "roa",
            "return on assets",
        ],
        "HAS_MARKET_CAP": [
            "market cap",
            "market capitalization",
        ],
        "HAS_PE_RATIO": [
            "pe ratio",
            "price earnings",
        ],
        "HAS_PB_RATIO": [
            "pb ratio",
            "price book",
        ],
        "HAS_DIVIDEND": [
            "dividend",
        ],
        "HAS_GROSS_NPA": [
            "gross npa",
        ],
        "HAS_NET_NPA": [
            "net npa",
        ],
        "HAS_CASA_RATIO": [
            "casa",
        ],
    }

    detected = []

    for relation, keywords in relation_map.items():

        for keyword in keywords:

            if keyword in question:

                detected.append(relation)
                break

    logger.info(
        "Detected %d relationship types.",
        len(detected),
    )

    return detected


def retrieve_graph_context(
    company_name: str,
    question: str,
    limit: int = 20,
) -> list[str]:
    """
    Retrieve graph triples relevant
    to the question.
    """

    if not company_name.strip():
        raise InvalidRequestException(
            "Company name cannot be empty."
        )

    if not question.strip():
        raise InvalidRequestException(
            "Question cannot be empty."
        )

    logger.info(
        "Retrieving graph context for company: %s",
        company_name,
    )

    driver = get_driver()

    relations = detect_relations(question)

    if relations:

        logger.info(
            "Filtering graph by %d relationship types.",
            len(relations),
        )

        query = """
        MATCH (source)-[r]->(target)
        WHERE
            toLower(source.name)
            CONTAINS toLower($company)
            AND
            type(r) IN $relations
        RETURN
            source.name AS source,
            type(r) AS relationship,
            target.name AS target
        LIMIT $limit
        """

        parameters = {
            "company": company_name,
            "relations": relations,
            "limit": limit,
        }

    else:

        logger.info(
            "No relationship filter detected. Retrieving all relationships."
        )

        query = """
        MATCH (source)-[r]->(target)
        WHERE
            toLower(source.name)
            CONTAINS toLower($company)
        RETURN
            source.name AS source,
            type(r) AS relationship,
            target.name AS target
        LIMIT $limit
        """

        parameters = {
            "company": company_name,
            "limit": limit,
        }

    graph_documents = []

    try:

        with driver.session() as session:

            results = session.run(
                query,
                **parameters,
            )

            for row in results:

                graph_documents.append(
                    f"{row['source']} "
                    f"{row['relationship']} "
                    f"{row['target']}"
                )

    except Neo4jError as error:

        logger.exception(
            "Neo4j query execution failed."
        )

        raise DatabaseException(
            f"Neo4j query failed: {error}"
        ) from error

    logger.info(
        "Retrieved %d graph triples.",
        len(graph_documents),
    )

    return graph_documents