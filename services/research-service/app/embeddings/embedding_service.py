"""
Embedding Service.

Generates vector embeddings
using the configured embedding model.
"""

import logging

from app.embeddings.embedding_model import (
    embedding_model,
)
from app.exceptions.custom_exceptions import (
    ExternalAPIException,
    InvalidRequestException,
)

logger = logging.getLogger(__name__)


def generate_embedding(
    text: str,
) -> list[float]:
    """
    Generate an embedding vector for the input text.

    Parameters
    ----------
    text : str
        Input text to embed.

    Returns
    -------
    list[float]
        Embedding vector.

    Raises
    ------
    InvalidRequestException
        If the input text is empty.

    ExternalAPIException
        If embedding generation fails.
    """

    if not text.strip():
        logger.warning(
            "Received empty text for embedding generation."
        )
        raise InvalidRequestException(
            "Input text cannot be empty."
        )

    logger.info(
        "Generating embedding."
    )

    try:

        embedding = embedding_model.encode(
            text
        )

        logger.info(
            "Embedding generated successfully."
        )

        return embedding.tolist()

    except Exception as error:

        logger.exception(
            "Embedding generation failed."
        )

        raise ExternalAPIException(
            f"Embedding generation failed: {error}"
        ) from error