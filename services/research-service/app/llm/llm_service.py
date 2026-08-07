"""
LLM Service.

Provides an interface for generating
responses using the Groq API.
"""

import logging

from app.database.config import settings
from app.exceptions.custom_exceptions import (
    LLMServiceException,
)
from groq import Groq

logger = logging.getLogger(__name__)

client = Groq(
    api_key=settings.GROQ_API_KEY
)


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
        If the Groq API request fails.
    """

    logger.info("Sending request to Groq LLM.")

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
        )

        answer = response.choices[0].message.content

        logger.info("Received response from Groq LLM.")

        return answer

    except Exception as error:

        logger.exception(
            "Groq LLM request failed."
        )

        raise LLMServiceException(
            str(error)
        ) from error


# Alias for compatibility
ask_llm = generate_answer