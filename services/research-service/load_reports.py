from app.report_ingestion.report_loader import (
    load_report
)


def main() -> None:

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
    pdf_path="app/database/reports/HDFC_Bank_Annual_Report_2024_25"
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