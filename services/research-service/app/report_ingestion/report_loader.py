"""
Generic report ingestion module.

Workflow
--------
PDF
 ↓
Extract Text
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
        Example:
        Q1, Q2, Q3, Q4

    Returns
    -------
    None
    """

    db = SessionLocal()

    try:

        # Extract text from PDF
        text = extract_pdf_text(
            pdf_path
        )

        # Save report metadata
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

        # Split into chunks
        chunks = split_into_chunks(
            text
        )

        # Store chunks
        for index, chunk in enumerate(chunks):

            document_chunk = DocumentChunk(
                report_id=report.id,
                chunk_number=index,
                chunk_text=chunk
            )

            db.add(document_chunk)

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


"""
Load reports into database.
"""

from app.report_ingestion.report_loader import (
    load_report
)


def main() -> None:
    """
    Load sample reports.
    """

    load_report(
        company_id=1,
        report_type="annual",
        year=2026,
        pdf_path="app/database/reports/infosys-ar-26.pdf"
    )

load_report(
    company_id=2,
    report_type="annual",
    year=2025,
    pdf_path="app/database/reports/HDFC_Bank_Annual_Report_2024_25.pdf"
)

load_report(
    company_id=4,
    report_type="annual",
    year=2025,
    pdf_path="app/database/reports/LNT_AR_Y2026.pdf"
)

load_report(
    company_id=1,
    report_type="annual",
    year=2025,
    pdf_path="app/database/reports/RIL-IAR-2025.pdf"
)

load_report(
    company_id=8,
    report_type="annual",
    year=2025,
    pdf_path="app/database/reports/tcs_report_2025-26.pdf"
)
if __name__ == "__main__":
    main()