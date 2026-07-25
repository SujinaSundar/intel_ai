"""
Hybrid GraphRAG prompt template.
"""


def build_hybrid_prompt(
    question: str,
    documents: list[str],
    graph_context: list[str],
    sentiment_text: str,
    stock_text: str
) -> str:
    """
    Build prompt for Hybrid GraphRAG.
    """

    report_context = "\n\n".join(documents)

    graph_info = "\n".join(graph_context)

    prompt = f"""
You are an expert financial research analyst.

Answer the user's question ONLY using the information provided below.

========================
REPORT CONTEXT
========================
{report_context}

========================
GRAPH KNOWLEDGE
========================
{graph_info}

========================
NEWS SENTIMENT
========================
{sentiment_text}

========================
STOCK DATA
========================
{stock_text}

========================
QUESTION
========================
{question}

Instructions:

1. Use the REPORT CONTEXT as the primary source of information.
2. Use GRAPH KNOWLEDGE to enrich the answer with company relationships, products, subsidiaries, partnerships, founders, and business entities.
3. Use NEWS SENTIMENT only to discuss recent market sentiment if it is relevant.
4. Use STOCK DATA only to mention recent trading performance when appropriate.
5. Do not use external knowledge.
6. Do not invent facts.
7. If information is unavailable, explicitly say so.

When summarizing a company, include (only if available):

- Company overview
- Core business
- Products and services
- Business segments
- Financial highlights
- AI / Digital initiatives
- Partnerships and subsidiaries
- Risks
- Future outlook

Provide a professional equity research style response.
"""

    return prompt