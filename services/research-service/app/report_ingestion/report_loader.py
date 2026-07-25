"""
Load report and store chunks.

Workflow
--------
PDF
 ↓
Extract Text
 ↓
Check Existing Report
 ↓
Save Report Metadata
 ↓
Chunk Text
 ↓
Save Chunks
"""

import logging

from sqlalchemy.exc import SQLAlchemyError

from app.database.connection import SessionLocal
from app.database.models import (
    DocumentChunk,
    ResearchReport,
)
from app.exceptions.custom_exceptions import (
    DatabaseException,
    ExternalAPIException,
    InvalidRequestException,
)
from app.report_ingestion.chunker import (
    split_into_chunks,
)
from app.report_ingestion.pdf_parser import (
    extract_pdf_text,
)

logger = logging.getLogger(__name__)


def load_report(
    company_id: int,
    report_type: str,
    year: int,
    pdf_path: str,
    quarter: str | None = None,
) -> None:
    """
    Load an annual or quarterly report.

    Parameters
    ----------
    company_id : int
        Company identifier.

    report_type : str
        Report type (annual or quarterly).

    year : int
        Financial year.

    pdf_path : str
        PDF file path.

    quarter : str | None
        Quarter information.

    Returns
    -------
    None
    """

    if company_id <= 0:
        raise InvalidRequestException(
            "Invalid company id."
        )

    if not pdf_path.strip():
        raise InvalidRequestException(
            "PDF path cannot be empty."
        )

    db = SessionLocal()

    try:

        logger.info(
            "Loading %s report for company %d (%d).",
            report_type,
            company_id,
            year,
        )

        # -----------------------------------
        # Check Existing Report
        # -----------------------------------

        existing_report = (
            db.query(ResearchReport)
            .filter(
                ResearchReport.company_id == company_id,
                ResearchReport.report_type == report_type,
                ResearchReport.year == year,
                ResearchReport.quarter == quarter,
            )
            .first()
        )

        if existing_report:

            logger.info(
                "Report already exists for company %d.",
                company_id,
            )

            return

        # -----------------------------------
        # Extract PDF Text
        # -----------------------------------

        try:

            text = extract_pdf_text(
                pdf_path
            )

            chunks = split_into_chunks(
                text
            )

        except Exception as error:

            logger.exception(
                "Failed to process PDF: %s",
                pdf_path,
            )

            raise ExternalAPIException(
                f"Failed to process PDF: {error}"
            ) from error

        logger.info(
            "Generated %d chunks.",
            len(chunks),
        )

        # -----------------------------------
        # Save Report Metadata
        # -----------------------------------

        report = ResearchReport(
            company_id=company_id,
            report_type=report_type,
            year=year,
            quarter=quarter,
            pdf_path=pdf_path,
        )

        db.add(report)

        db.commit()

        db.refresh(report)

        logger.info(
            "Research report created with id %d.",
            report.id,
        )

        # -----------------------------------
        # Store Chunks
        # -----------------------------------

        for index, chunk in enumerate(chunks):

            db.add(
                DocumentChunk(
                    report_id=report.id,
                    chunk_number=index,
                    chunk_text=chunk,
                )
            )

        db.commit()

        logger.info(
            "%d chunks stored successfully.",
            len(chunks),
        )

    except SQLAlchemyError as error:

        db.rollback()

        logger.exception(
            "Database error while loading report."
        )

        raise DatabaseException(
            f"Failed to load report: {error}"
        ) from error

    finally:

        db.close()

        logger.info(
            "Database session closed."
        )