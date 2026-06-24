"""
PDF text extraction utility.
"""

import re

import fitz


def extract_pdf_text(
    pdf_path: str
) -> str:
    """
    Extract and clean text from a PDF.

    Parameters
    ----------
    pdf_path : str
        PDF location.

    Returns
    -------
    str
        Cleaned PDF text.
    """

    text = ""

    document = fitz.open(
        pdf_path
    )

    try:

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
                    line
                ):
                    continue

                # Remove patterns like:
                # | 34 |
                # 34 |
                # | 34
                if re.fullmatch(
                    r"\|?\s*\d+\s*\|?",
                    line
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
                    or "Integrated Annual Report" in line
                ):
                    continue

                # Remove very short noise
                if len(line) < 4:
                    continue

                # Normalize spaces
                line = re.sub(
                    r"\s+",
                    " ",
                    line
                )

                clean_lines.append(
                    line
                )

            page_clean_text = "\n".join(
                clean_lines
            )

            text += page_clean_text
            text += "\n"

    finally:

        document.close()

    return text