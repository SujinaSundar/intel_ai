"""
Company extractor for GraphRAG.
"""

from app.database.connection import (
    SessionLocal
)

from app.database.models import (
    Company
)


def extract_company(
    question: str
) -> str | None:
    """
    Extract company name from user question.
    """

    db = SessionLocal()

    try:

        companies = (
            db.query(
                Company
            )
            .all()
        )

        question = question.lower()

        for company in companies:

            company_name = (
                company.company_name
            ).lower()

            if company_name in question:

                return company.company_name

            first_word = (
                company_name.split()[0]
            )

            if first_word in question:

                return company.company_name

        return None

    finally:

        db.close()