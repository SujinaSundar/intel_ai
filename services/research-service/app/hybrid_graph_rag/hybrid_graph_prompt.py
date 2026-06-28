"""
Hybrid Graph Prompt.
"""


def build_hybrid_graph_prompt(
    question: str,
    documents: list[str],
    graph_documents: list[str],
    sentiment_text: str,
    stock_text: str
) -> str:
    """
    Build Hybrid GraphRAG prompt.
    """

    document_context = "\n".join(
        documents
    )

    graph_context = "\n".join(
        graph_documents
    )

    return f"""
You are a financial research assistant.

Use ONLY the information provided below.

Rules
-----

1. Prefer explicit facts from Graph Context.

2. Use Document Context only when
   Graph Context does not contain
   the required information.

3. Do NOT infer relationships.

4. Do NOT assume facts.

5. Do NOT use external knowledge.

6. If information is not explicitly
   available, respond:

   "Information unavailable."

7. For relationship questions,
   prioritize Graph Context.

8. For factual details such as
   policies, products, services,
   financial information,
   use Document Context when needed.

9. When possible, cite the exact
   relationship found in the graph.

Graph Context
-------------
{graph_context}

Document Context
----------------
{document_context}

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