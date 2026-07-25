"""
Test LangGraph Workflow.
"""

from app.langgraph.workflow import WorkflowRunner


def main():
    """
    Test LangGraph.
    """

    runner = WorkflowRunner()

    print()

    print("=" * 80)

    print(
        "LangGraph Trading Research Agent"
    )

    print("=" * 80)

    while True:

        question = input(

            "\nAsk a question (exit to quit): "

        )

        if question.lower() == "exit":

            break

        print()

        response = runner.run(
            question
        )

        print(response)


if __name__ == "__main__":

    main()