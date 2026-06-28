"""
GraphRAG prompt template.
"""


def build_graph_prompt(
    question: str,
    graph_documents: list[str]
) -> str:
    """
    Build GraphRAG prompt.
    """

    if graph_documents:

        graph_context = "\n".join(
            graph_documents
        )

    else:

        graph_context = (
            "No graph relationships found."
        )

    prompt = f"""
You are a financial research assistant.

Answer ONLY using the graph
relationships provided below.

Do not use external knowledge.

If the answer cannot be found,
say:

"Information unavailable in graph."

Graph Context
-------------

{graph_context}

Question
--------

{question}

Answer:
"""

    return prompt