from app.graph_rag.relation_extractor import (
    extract_relations
)


def main():

    text = """

    HDFC Bank has a board approved
    Information Security Policy
    and Cybersecurity Policy.

    """

    triples = extract_relations(
        text
    )

    print()

    print(
        triples
    )


if __name__ == "__main__":

    main()