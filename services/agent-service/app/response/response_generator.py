"""
Response Generator.

Converts structured JSON
returned by Agents into
a professional natural
language response using
an LLM.
"""

import logging
from typing import Any

from app.exceptions.custom_exceptions import (
    InvalidRequestException,
    LLMServiceException,
)
from app.llm.llm_service import (
    generate_answer,
)
from app.prompts.response_prompt import (
    get_response_prompt,
)

logger = logging.getLogger(__name__)


class ResponseGenerator:
    """
    Response Generator.

    Uses the LLM to convert
    structured JSON into a
    readable response.
    """

    def generate(
        self,
        question: str,
        data: dict[str, Any],
    ) -> str:
        """
        Generate the final
        natural language response.

        Parameters
        ----------
        question : str
            User question.

        data : dict[str, Any]
            Structured agent response.

        Returns
        -------
        str
            LLM-generated response.

        Raises
        ------
        InvalidRequestException
            If the question or data is invalid.

        LLMServiceException
            If the LLM returns an empty response.
        """

        if not question or not question.strip():

            logger.warning(
                "Empty question received."
            )

            raise InvalidRequestException(
                "Question cannot be empty."
            )

        if not data:

            logger.warning(
                "Empty response data received."
            )

            raise InvalidRequestException(
                "Response data cannot be empty."
            )

        logger.info(
            "Generating final response."
        )

        prompt = get_response_prompt(
            question,
            data,
        )

        logger.debug(
            "Response prompt generated successfully."
        )

        response = generate_answer(
            prompt
        )

        if not response or not response.strip():

            logger.error(
                "LLM returned an empty response."
            )

            raise LLMServiceException(
                "Failed to generate response."
            )

        logger.info(
            "Response generated successfully."
        )

        return response

    def health_check(
        self,
    ) -> dict[str, str]:
        """
        Check Response Generator
        health status.

        Returns
        -------
        dict[str, str]
            Generator status.
        """

        logger.info(
            "Response Generator health check."
        )

        return {
            "response_generator": "Available"
        }


response_generator = ResponseGenerator()