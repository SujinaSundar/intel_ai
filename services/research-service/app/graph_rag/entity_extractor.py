"""
Entity extraction for GraphRAG.

Extract entities from report chunks.
"""

import re


def extract_entities(
    text: str
) -> list[str]:
    """
    Extract capitalized entities.

    Parameters
    ----------
    text : str

    Returns
    -------
    list[str]
    """

    entities = re.findall(

        r"\b[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*\b",

        text
    )

    return list(
        set(
            entities
        )
    )