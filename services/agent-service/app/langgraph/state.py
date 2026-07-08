"""
LangGraph State.

Defines the shared state
used throughout the
LangGraph workflow.
"""

from typing import TypedDict
from typing import Optional
from typing import Any


class AgentState(TypedDict):
    """
    Shared workflow state.

    Every node can read
    and update this state.
    """

    # User question

    question: str

    # Router output

    route: Optional[dict]

    # Agent output

    agent_response: Optional[Any]

    # Final response

    final_response: Optional[str]