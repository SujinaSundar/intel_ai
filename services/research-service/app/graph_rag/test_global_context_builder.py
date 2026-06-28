from app.graph_rag.global_graph_context_builder import (
    build_global_graph_context
)


def main():

    context = (
        build_global_graph_context()
    )

    print()

    print(
        f"Relationships: "
        f"{len(context['graph_documents'])}"
    )

    print()

    for doc in context[
        "graph_documents"
    ][:20]:

        print(doc)


if __name__ == "__main__":

    main()