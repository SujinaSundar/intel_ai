"""
Chat Service.

Executes the LangGraph
workflow for frontend
requests.
"""

import logging

from app.exceptions.custom_exceptions import (
    AppException,
    InvalidRequestException,
    LLMServiceException,
)
from app.langgraph.workflow import WorkflowRunner

logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# Workflow Runner
# ---------------------------------------------------------

workflow = WorkflowRunner()


# ---------------------------------------------------------
# Execute Workflow
# ---------------------------------------------------------

def ask_question(
    question: str,
    history: list[dict[str, str]],
    user_id: int,
) -> str:
    """
    Execute the LangGraph workflow.

    Parameters
    ----------
    question : str
        User research question.

    history : list[dict[str, str]]
        Previous conversation
        history.

    user_id : int
        Authenticated user ID.

    Returns
    -------
    str
        Final response generated
        by the LangGraph workflow.

    Raises
    ------
    InvalidRequestException
        If the question is empty.

    AppException
        Re-raises known application exceptions.

    LLMServiceException
        If an unexpected error occurs while processing
        the request.
    """

    logger.info(
        "Processing chat request | user_id=%s",
        user_id,
    )

    # -----------------------------------------------------
    # Validate Request
    # -----------------------------------------------------

    if not question or not question.strip():

        logger.warning(
            "Empty question received | user_id=%s",
            user_id,
        )

        raise InvalidRequestException(
            "Question cannot be empty."
        )

    try:

        answer = workflow.run(
            question=question,
            history=history,
        )

        logger.info(
            "Workflow completed successfully | user_id=%s",
            user_id,
        )

        return answer

    except AppException:
        # Re-raise known application exceptions
        raise

    except Exception as error:

        logger.exception(
            "Workflow execution failed | user_id=%s",
            user_id,
        )

        raise LLMServiceException(
            "Failed to process the request."
        ) from error