"""
PDF text extraction utility.
"""

import re

import fitz
from app.exceptions.custom_exceptions import (
    ExternalAPIException,
    InvalidRequestException,
)


def extract_pdf_text(
    pdf_path: str,
) -> str:
    """
    Extract and clean text from a PDF.

    Parameters
    ----------
    pdf_path : str
        PDF file path.

    Returns
    -------
    str
        Cleaned PDF text.
    """

    if not pdf_path or not pdf_path.strip():
        raise InvalidRequestException(
            "PDF path cannot be empty."
        )

    try:

        text = ""

        with fitz.open(pdf_path) as document:

            for page in document:

                page_text = page.get_text()

                lines = page_text.split(
                    "\n"
                )

                clean_lines = []

                for line in lines:

                    line = line.strip()

                    # Empty lines
                    if not line:
                        continue

                    # Page numbers
                    if re.fullmatch(
                        r"\d+",
                        line,
                    ):
                        continue

                    # Remove patterns like:
                    # | 34 |
                    # 34 |
                    # | 34
                    if re.fullmatch(
                        r"\|?\s*\d+\s*\|?",
                        line,
                    ):
                        continue

                    # URLs
                    if (
                        line.startswith("http")
                        or "www." in line
                    ):
                        continue

                    # Annual report headers
                    if (
                        "Annual Report" in line
                        or "Integrated Annual Report"
                        in line
                    ):
                        continue

                    # Remove very short noise
                    if len(line) < 4:
                        continue

                    # Normalize whitespace
                    line = re.sub(
                        r"\s+",
                        " ",
                        line,
                    )

                    clean_lines.append(
                        line
                    )

                text += (
                    "\n".join(clean_lines)
                    + "\n"
                )

        return text

    except Exception as error:

        raise ExternalAPIException(
            f"Failed to extract PDF text: {error}"
        ) from error