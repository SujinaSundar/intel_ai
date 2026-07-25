"""
Company Extractor for GraphRAG.

Extracts the company name mentioned
in a user question.
"""

import logging

from app.database.connection import (
    SessionLocal,
)
from app.database.models import (
    Company,
)
from app.exceptions.custom_exceptions import (
    DatabaseException,
    InvalidRequestException,
)
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


def extract_company(
    question: str,
) -> str | None:
    """
    Extract the company name from a user question.

    Parameters
    ----------
    question : str
        User question.

    Returns
    -------
    str | None
        Company name if found, otherwise None.
    """

    if not question or not question.strip():
        raise InvalidRequestException(
            "Question cannot be empty."
        )

    logger.info(
        "Extracting company from user question."
    )

    db = SessionLocal()

    try:

        companies = (
            db.query(Company)
            .all()
        )

        question = question.lower()

        for company in companies:

            company_name = company.company_name.lower()

            if company_name in question:

                logger.info(
                    "Matched company: %s",
                    company.company_name,
                )

                return company.company_name

            first_word = company_name.split()[0]

            if first_word in question:

                logger.info(
                    "Matched company using first word: %s",
                    company.company_name,
                )

                return company.company_name

        logger.info(
            "No company detected in question."
        )

        return None

    except SQLAlchemyError as error:

        logger.exception(
            "Failed to retrieve companies from database."
        )

        raise DatabaseException(
            f"Company extraction failed: {error}"
        ) from error

    finally:

        db.close()

        logger.debug(
            "Database session closed."
        )