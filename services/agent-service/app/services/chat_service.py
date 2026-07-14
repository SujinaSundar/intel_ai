from app.langgraph.workflow import WorkflowRunner

runner = WorkflowRunner()


def ask_question(question: str) -> str:
    """
    Execute LangGraph workflow.
    """

    return runner.run(question)