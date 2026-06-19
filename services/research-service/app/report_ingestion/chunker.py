from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


def split_into_chunks(
        text: str
) -> list[str]:
    """
    Split text into chunks.

    Parameters
    ----------
    text : str

    Returns
    -------
    list[str]
    """

    splitter = (
        RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    )

    return splitter.split_text(text)