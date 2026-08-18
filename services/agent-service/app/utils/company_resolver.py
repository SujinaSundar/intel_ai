"""
Company Resolver.


Resolves company names
from the current question
or conversation history.
"""


PRONOUNS = (
    " it ",
    " it's ",
    " its ",
    " they ",
    " them ",
    " their ",
    " this ",
    " that ",
    " company ",
)


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


    question_lower = f" {question.lower()} "


    # ---------------------------------------------
    # Explicit company in current question
    # ---------------------------------------------


    for company in COMPANIES:


        if company.lower() in question_lower:


            return company


    # ---------------------------------------------
    # Pronoun reference?
    # ---------------------------------------------


    uses_reference = any(
        pronoun in question_lower
        for pronoun in PRONOUNS
    )


    if not uses_reference:


        return None


    # ---------------------------------------------
    # Find latest company in history
    # ---------------------------------------------


    for message in reversed(history):


        content = message.get(
            "content",
            "",
        ).lower()


        for company in COMPANIES:


            if company.lower() in content:


                return company


    return None
