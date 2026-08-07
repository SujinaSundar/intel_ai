"""
Company Resolver.

Resolves company names
from the current question
or conversation history.
"""


COMPANIES = [
    "Infosys",
    "TCS",
    "Reliance Industries",
    "HDFC Bank",
    "ICICI Bank",
    "Wipro",
    "Axis Bank",
    "SBI",
    "ITC",
    "Bharti Airtel",
    "Larsen & Toubro",
]


def resolve_company(
    question: str,
    history: list[dict[str, str]] | None = None,
) -> str | None:
    """
    Resolve the company name from the
    current question or conversation history.
    """

    history = history or []

    text = question.lower()

    # -------------------------------------------------
    # Search current question
    # -------------------------------------------------

    for company in COMPANIES:

        if company.lower() in text:
            return company

    # -------------------------------------------------
    # Search conversation history (latest first)
    # -------------------------------------------------

    for message in reversed(history):

        content = message.get(
            "content",
            "",
        ).lower()

        for company in COMPANIES:

            if company.lower() in content:
                return company

    return None