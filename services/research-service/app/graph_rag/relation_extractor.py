"""
Relation extractor.

Uses LLM to extract
knowledge graph triples.
"""

import json

from app.llm.llm_service import (
    generate_answer
)


def extract_relations(
    text: str
) -> list:
    """
    Extract graph triples.

    Parameters
    ----------
    text : str

    Returns
    -------
    list
    """

    prompt = f"""
You are an expert financial knowledge graph builder.

Your job is to extract ONLY meaningful
business relationships from company reports,
annual reports, quarterly reports,
corporate disclosures, and financial news.

Return ONLY valid JSON.

Rules
-----

1. Extract ONLY business-relevant relationships.

Focus on:

- CEO
- Founder
- Managing Director
- Chairman
- Product
- Platform
- Service
- Technology
- AI Initiative
- Partnership
- Acquisition
- Merger
- Subsidiary
- Investment
- Industry
- Sector
- Customer
- Vendor
- Strategic Initiative

2. Ignore:

- lease disclosures
- accounting policies
- depreciation notes
- audit notes
- tax disclosures
- employee compensation notes
- financial statement notes
- accounting standards
- legal boilerplate
- generic governance disclosures
- risk disclosures without entities
- generic financial reporting text

3. Use concise UPPERCASE relationship names.

Examples:

HAS_CEO
HAS_PRODUCT
HAS_SERVICE
HAS_PLATFORM
HAS_TECHNOLOGY
PARTNERS_WITH
BELONGS_TO
ACQUIRED
INVESTS_IN
SERVES
OWNS
MANAGES
LAUNCHED
FOCUSES_ON
PROVIDES
SUBSIDIARY_OF

4. Do NOT use generic relationships.

Avoid:

has
contains
includes
related_to
mentions

5. Entity types must be one of:

Company
Person
Product
Service
Technology
Platform
Sector
Industry
Organization
Bank
Customer
Vendor
Initiative
Policy

6. If no meaningful business relationship exists,
return:

[]

7. Return ONLY JSON.

Format
------

[
  {{
    "source":"Infosys",
    "source_type":"Company",
    "relation":"HAS_CEO",
    "target":"Salil Parekh",
    "target_type":"Person"
  }}
]

Text
----

{text[:1500]}
"""

    response = generate_answer(
        prompt
    )

    try:

        return json.loads(
            response
        )

    except Exception as error:

        print()

        print(
            "Relation extraction failed."
        )

        print(
            error
        )

        print()

        print(
            "LLM Response:"
        )

        print(
            response
        )

        return []