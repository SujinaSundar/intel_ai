"""
Relation Extractor.

Extracts high-confidence business
relationships from annual report chunks.
"""

import json
import logging

from app.exceptions.custom_exceptions import (
    InvalidRequestException,
    LLMServiceException,
)
from app.llm.llm_service import (
    generate_answer,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# Allowed Relationships
# ---------------------------------------------------------

ALLOWED_RELATIONS = {
    # Leadership
    "HAS_CEO",
    "HAS_CFO",
    "HAS_CHAIRMAN",
    "HAS_MANAGING_DIRECTOR",
    "HAS_FOUNDER",

    # Products & Services
    "HAS_PRODUCT",
    "HAS_SERVICE",
    "HAS_PLATFORM",
    "HAS_TECHNOLOGY",
    "PROVIDES",
    "OFFERS",

    # Strategy
    "FOCUSES_ON",
    "OPERATES_IN",
    "SERVES",
    "EXPANDS_TO",

    # Corporate
    "PARTNERS_WITH",
    "ACQUIRED",
    "SUBSIDIARY_OF",
    "INVESTS_IN",
    "BELONGS_TO",

    # Innovation
    "DEVELOPS",
    "USES",
    "LAUNCHED",

    # ESG
    "SUPPORTS",
    "PROMOTES",
    "REDUCES_EMISSIONS",
}

# ---------------------------------------------------------
# Generic Target Entities
# ---------------------------------------------------------

GENERIC_TARGETS = {
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
    "technologies",
    "platform",
    "platforms",
    "solution",
    "solutions",
    "initiative",
    "initiatives",
    "market",
    "markets",
    "industry",
    "industries",
}


# ---------------------------------------------------------
# Clean LLM Response
# ---------------------------------------------------------

def clean_llm_response(
    response: str,
) -> str:
    """
    Clean markdown formatting from the
    LLM response and extract the JSON array.

    Parameters
    ----------
    response : str
        Raw LLM response.

    Returns
    -------
    str
        Clean JSON string or an empty string
        if no JSON array is found.
    """

    if not response or not response.strip():
        raise InvalidRequestException(
            "LLM response cannot be empty."
        )

    response = response.strip()

    response = response.replace(
        "```json",
        "",
    )

    response = response.replace(
        "```",
        "",
    )

    response = response.strip()

    start = response.find("[")

    end = response.rfind("]")

    if start == -1 or end == -1:

        logger.warning(
            "No JSON array found in LLM response."
        )

        return ""

    cleaned_response = response[start : end + 1]

    logger.debug(
        "Successfully cleaned LLM response."
    )

    return cleaned_response
# ---------------------------------------------------------
# Relation Extraction
# ---------------------------------------------------------

def extract_relations(
    company_name: str,
    text: str,
) -> list[dict]:
    """
    Extract business relationships from
    a report chunk using the LLM.

    Parameters
    ----------
    company_name : str
        Company name.

    text : str
        Annual report chunk.

    Returns
    -------
    list[dict]
        Validated graph triples.
    """

    if not company_name.strip():
        raise InvalidRequestException(
            "Company name cannot be empty."
        )

    if not text.strip():
        raise InvalidRequestException(
            "Report text cannot be empty."
        )

    logger.info(
        "Extracting relations for company: %s",
        company_name,
    )

    prompt = f"""
You are an expert Financial Knowledge Graph Builder.

The following text belongs ONLY to the annual report of

{company_name}

Your task is to extract ONLY business relationships where

{company_name}

is the SOURCE entity.

Rules

1. Return ONLY JSON.

2. Return between 1 and 5 HIGH-CONFIDENCE relationships.

If no meaningful business relationship exists, return [].

Do not guess or infer missing information.

3. Ignore unrelated companies.

4. Ignore financial metrics.

5. Ignore accounting notes.

6. Ignore audit notes.

7. Ignore legal disclosures.

8. Ignore tables.

9. Ignore historical examples.

10. Never invent facts.

11. Every relationship must be explicitly supported by the text.

Allowed Relations

{", ".join(sorted(ALLOWED_RELATIONS))}

Output Format

[
    {{
        "source":"{company_name}",
        "source_type":"Company",
        "relation":"HAS_PRODUCT",
        "target":"Finacle",
        "target_type":"Product"
    }}
]

TEXT

{text[:2500]}
"""

    try:

        response = generate_answer(prompt)

    except LLMServiceException:

        logger.exception(
            "LLM relation extraction failed."
        )

        raise

    cleaned_response = clean_llm_response(
        response
    )

    if not cleaned_response:

        logger.info(
            "No relations returned by LLM."
        )

        return []

    try:

        relations = json.loads(
            cleaned_response
        )

    except json.JSONDecodeError:

        logger.exception(
            "Invalid JSON returned from LLM."
        )

        logger.debug(
            "LLM Response: %s",
            cleaned_response,
        )

        return []

    if not isinstance(relations, list):

        logger.warning(
            "LLM output is not a list."
        )

        return []

    unique = []

    seen = set()

    for relation in relations:

        try:

            required_fields = {
                "source",
                "source_type",
                "relation",
                "target",
                "target_type",
            }

            if not required_fields.issubset(
                relation.keys()
            ):
                continue

            source = (
                relation["source"]
                .strip()
            )

            source_type = (
                relation["source_type"]
                .strip()
            )

            relation_name = (
                relation["relation"]
                .strip()
                .upper()
            )

            target = (
                relation["target"]
                .strip()
            )

            target_type = (
                relation["target_type"]
                .strip()
            )

            # -------------------------------------
            # Keep only current company
            # -------------------------------------

            if (
                source.lower()
                != company_name.lower()
            ):
                continue

            source = company_name

            # -------------------------------------
            # Allowed relation
            # -------------------------------------

            if (
                relation_name
                not in ALLOWED_RELATIONS
            ):
                continue

            # -------------------------------------
            # Empty target
            # -------------------------------------

            if not target:
                continue

            # -------------------------------------
            # Generic entity
            # -------------------------------------

            if (
                target.lower()
                in GENERIC_TARGETS
            ):
                continue

            # -------------------------------------
            # Self-loop
            # -------------------------------------

            if (
                target.lower()
                == company_name.lower()
            ):
                continue

            # -------------------------------------
            # Normalize entity names
            # -------------------------------------

            if target_type in {
                "Product",
                "Service",
                "Technology",
                "Platform",
                "Industry",
                "Sector",
            }:
                target = target.title()

            key = (
                source.lower(),
                relation_name,
                target.lower(),
            )

            if key in seen:
                continue

            seen.add(key)

            unique.append(
                {
                    "source": source,
                    "source_type": source_type,
                    "relation": relation_name,
                    "target": target,
                    "target_type": target_type,
                }
            )

        except Exception:

            logger.exception(
                "Skipping invalid relation."
            )

            continue

    logger.info(
        "Extracted %d valid relations.",
        len(unique),
    )

    return unique