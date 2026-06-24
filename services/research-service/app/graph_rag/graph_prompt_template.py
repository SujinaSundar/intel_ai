"""
GraphRAG prompt template.
"""


def build_graph_prompt(
    question: str,
    graph_documents: list[str],
    sentiment_text: str,
    stock_text: str
) -> str:
    """
    Build GraphRAG prompt.
    """

    graph_context = "\n".join(
        graph_documents
    )

    prompt = f"""
You are a financial research assistant.

Use ONLY the information provided below.

Use graph relationships, sentiment information and stock data.

Do not use external knowledge.

Do not make definitive investment recommendations.

If information is unavailable, explicitly say so.

Graph Context
-------------
{graph_context}

Sentiment
---------
{sentiment_text}

Stock Information
-----------------
{stock_text}

Question
--------
{question}

Answer:
"""

    return prompt