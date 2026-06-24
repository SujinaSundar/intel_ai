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

from app.database.connection import SessionLocal

from app.database.models import (
    ResearchReport,
    DocumentChunk
)

from app.report_ingestion.pdf_parser import (
    extract_pdf_text
)

from app.report_ingestion.chunker import (
    split_into_chunks
)


def load_report(
    company_id: int,
    report_type: str,
    year: int,
    pdf_path: str,
    quarter: str | None = None
) -> None:
    """
    Load annual or quarterly report.

    Parameters
    ----------
    company_id : int
        Company id.

    report_type : str
        annual or quarterly.

    year : int
        Financial year.

    pdf_path : str
        PDF location.

    quarter : str | None
        Quarter information.

    Returns
    -------
    None
    """

    db = SessionLocal()

    try:

        # Check whether report already exists
        existing_report = (
            db.query(ResearchReport)
            .filter(
                ResearchReport.company_id == company_id,
                ResearchReport.report_type == report_type,
                ResearchReport.year == year,
                ResearchReport.quarter == quarter
            )
            .first()
        )

        if existing_report:

            print(
                f"Report already exists "
                f"(Company {company_id}, "
                f"{report_type}, {year})."
            )

            return

        # Extract text
        text = extract_pdf_text(
            pdf_path
        )

        # Save metadata
        report = ResearchReport(
            company_id=company_id,
            report_type=report_type,
            year=year,
            quarter=quarter,
            pdf_path=pdf_path
        )

        db.add(report)

        db.commit()

        db.refresh(report)

        # Generate chunks
        chunks = split_into_chunks(
            text
        )

        print(
            f"Generated {len(chunks)} chunks."
        )

        # Store chunks
        for index, chunk in enumerate(chunks):

            document_chunk = DocumentChunk(
                report_id=report.id,
                chunk_number=index,
                chunk_text=chunk
            )

            db.add(
                document_chunk
            )

        db.commit()

        print(
            f"{len(chunks)} chunks inserted successfully."
        )

    except Exception as error:

        db.rollback()

        print(
            f"Error loading report: {error}"
        )

    finally:

        db.close()