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

1. URules
-----

1. Use BOTH Graph Context and Document Context together.

2. Graph Context contains structured business
   relationships such as:
   CEO, products, services, partnerships,
   acquisitions, subsidiaries and focus areas.

3. Document Context contains detailed financial
   information such as annual report content,
   business strategy, financial performance,
   risks, policies and other descriptive text.

4. Combine information from both contexts
   whenever they complement each other.

5. For relationship-based questions,
   prioritize Graph Context.

6. For financial facts, explanations,
   numerical values and report details,
   prioritize Document Context.

7. Do NOT assume facts.

8. Do NOT use external knowledge.

9. If the answer cannot be found in either
   context, reply exactly:

   "Information unavailable."

10. When answering relationship questions,
    mention the exact relationship when possible.

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