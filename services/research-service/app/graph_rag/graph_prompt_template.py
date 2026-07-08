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
You are an expert financial research assistant.

Use ONLY the graph relationships provided below.

Instructions
------------
1. Read all graph relationships carefully.
2. Combine related relationships into one coherent answer.
3. Do NOT simply repeat the graph triples.
4. Write a natural language response.
5. If multiple relationships exist, summarize them together.
6. If the information is unavailable, reply:
   "Information unavailable in graph."

Graph Relationships
-------------------

{graph_context}

Question
--------

{question}

Answer
------
"""

    return prompt