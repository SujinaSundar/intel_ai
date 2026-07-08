"""
Response Generator.

Converts structured JSON
returned by Agents into
a professional natural
language response using
an LLM.
"""

from app.llm.llm_service import (
    generate_answer
)

from app.prompts.response_prompt import (
    get_response_prompt
)


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
        data: dict
    ) -> str:
        """
        Generate final response.

        Parameters
        ----------
        question : str

        data : dict

        Returns
        -------
        str
        """

        prompt = get_response_prompt(

            question,

            data

        )

        response = generate_answer(

            prompt

        )

        return response

    def health_check(
        self
    ) -> dict:
        """
        Check generator status.

        Returns
        -------
        dict
        """

        return {

            "response_generator":

                "Available"

        }