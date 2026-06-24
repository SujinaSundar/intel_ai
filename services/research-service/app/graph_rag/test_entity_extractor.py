"""
Test entity extraction.
"""

from app.graph_rag.entity_extractor import (
    extract_entities
)


def main():

    text = """
    Infosys Topaz is an enterprise AI platform.

    Salil Parekh is the CEO of Infosys.

    Infosys partners with Microsoft.
    """

    entities = extract_entities(
        text
    )

    print()

    print(
        "Entities"
    )

    print(
        "-" * 50
    )

    for entity in entities:

        print(
            entity
        )


if __name__ == "__main__":

    main()