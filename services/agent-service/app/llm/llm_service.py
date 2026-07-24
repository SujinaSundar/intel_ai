"""
LLM Service.

Provides utility functions for interacting with the
Groq Large Language Model.
"""

import logging

from groq import Groq

from app.database.config import settings
from app.exceptions.custom_exceptions import (
    LLMServiceException,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# Groq Client
# ---------------------------------------------------------

client = Groq(
    api_key=settings.GROQ_API_KEY
)

# ---------------------------------------------------------
# Generate Answer
# ---------------------------------------------------------

def generate_answer(
    prompt: str,
) -> str:
    """
    Generate an answer using the Groq LLM.

    Parameters
    ----------
    prompt : str
        Prompt sent to the language model.

    Returns
    -------
    str
        Generated response from the LLM.

    Raises
    ------
    LLMServiceException
        If the LLM request fails or returns an
        invalid response.
    """

    logger.info("Sending request to Groq LLM.")

    # -----------------------------------------------------
    # Validate Input
    # -----------------------------------------------------

    if not prompt or not prompt.strip():
        logger.warning("Empty prompt received.")

        raise LLMServiceException(
            "Prompt cannot be empty."
        )

    try:

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],

            temperature=0,
        )

        answer = (
            response
            .choices[0]
            .message.content
        )

        if not answer:

            logger.error(
                "Groq returned an empty response."
            )

            raise LLMServiceException(
                "LLM returned an empty response."
            )

        logger.info("Groq response generated successfully.")

        return answer

    except LLMServiceException:
        raise

    except Exception as error:

        logger.exception(
            "Groq request failed."
        )

        raise LLMServiceException(
            "Unable to generate response from the language model."
        ) from error


# ---------------------------------------------------------
# Alias
# ---------------------------------------------------------

# Alias for compatibility
ask_llm = generate_answer