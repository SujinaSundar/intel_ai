import fitz


def extract_pdf_text(
    pdf_path: str
) -> str:
    """
    Extract all text from a PDF.

    Parameters
    ----------
    pdf_path : str
        PDF location.

    Returns
    -------
    str
        Complete extracted text.
    """

    text = ""

    document = fitz.open(pdf_path)

    for page in document:

        text += page.get_text()

    document.close()

    return text