"""
Hybrid Graph Prompt Builder.

Builds the prompt for the Hybrid GraphRAG
pipeline by combining vector retrieval,
graph retrieval, market sentiment, and
stock information.
"""


def build_hybrid_graph_prompt(
    question: str,
    documents: list[str],
    graph_documents: list[str],
    sentiment_text: str,
    stock_text: str,
) -> str:
    """
    Build the Hybrid GraphRAG prompt.

    Parameters
    ----------
    question : str
        User question.

    documents : list[str]
        Retrieved document chunks.

    graph_documents : list[str]
        Retrieved graph relationships.

    sentiment_text : str
        News sentiment summary.

    stock_text : str
        Stock information summary.

    Returns
    -------
    str
        Prompt for the LLM.
    """

    document_context = "\n".join(
        documents
    )

    graph_context = "\n".join(
        graph_documents
    )

    # -----------------------------------
    # Optional Market Context
    # -----------------------------------

    market_sections: list[str] = []

    if sentiment_text:

        market_sections.append(
            f"""News Sentiment
--------------
{sentiment_text}"""
        )

    if stock_text:

        market_sections.append(
            f"""Stock Information
-----------------
{stock_text}"""
        )

    market_context = ""

    if market_sections:

        market_context = (
            "\n\n"
            + "\n\n".join(
                market_sections
            )
        )

    return f"""You are a financial research assistant.

Use ONLY the information provided below.

Rules
-----

1. Use BOTH Graph Context and Document Context together.

2. Graph Context contains structured business
   relationships such as:
   CEO, products, services, partnerships,
   acquisitions, subsidiaries and focus areas.

3. Document Context contains detailed business
   information such as:
   annual reports, financial performance,
   business strategy, risks, ESG initiatives,
   technologies and management discussion.

4. Combine Graph Context and Document Context
   whenever they complement each other.

5. For relationship-based questions,
   prioritize Graph Context.

6. For detailed explanations,
   business strategy,
   financial facts and report content,
   prioritize Document Context.

7. Market Context (if provided)
   contains recent stock information
   and news sentiment.

8. Use Market Context ONLY when it is
   relevant to the user's question.

9. Do NOT assume facts.

10. Do NOT use external knowledge.

11. If the answer cannot be found in the
    provided context, reply exactly:

    "Information unavailable."

12. When answering relationship questions,
    mention the relationship whenever possible.

Graph Context
-------------
{graph_context}

Document Context
----------------
{document_context}{market_context}

Question
--------
{question}

Answer:
"""