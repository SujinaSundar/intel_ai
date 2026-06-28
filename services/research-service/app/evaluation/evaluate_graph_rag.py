from app.graph_rag.global_graph_rag_pipeline import (
    ask_global_graph_question
)

TEST_CASES = TEST_CASES = [

    # Direct Retrieval

    {
        "question": "What does HDFC Bank focus on?",
        "expected": "Banking"
    },

    {
        "question": "What industries does Reliance Industries focus on?",
        "expected": "Energy"
    },

    {
        "question": "What policies are associated with HDFC Bank?",
        "expected": "Information Security Policy"
    },

    # Relationship

    {
        "question": "Which companies focus on Banking?",
        "expected": "HDFC Bank"
    },

    {
        "question": "Which companies have acquisitions?",
        "expected": "HDFC Bank"
    },

    # Comparison

    {
        "question": "Compare HDFC Bank and Reliance Industries.",
        "expected": "Banking"
    },

    {
        "question": "Which companies focus on more than one industry?",
        "expected": "Reliance Industries"
    }

]


def evaluate():

    correct = 0

    total = len(TEST_CASES)

    for test in TEST_CASES:

        answer = ask_global_graph_question(
            test["question"]
        )

        expected = test["expected"]

        passed = (
            expected.lower()
            in answer.lower()
        )

        if passed:

            correct += 1

        print()
        print("=" * 80)

        print(
            test["question"]
        )

        print()

        print(
            "Expected:",
            expected
        )

        print()

        print(
            "Answer:",
            answer
        )

        print()

        print(
            "PASS"
            if passed
            else
            "FAIL"
        )

    print()

    print("=" * 80)

    print(
        f"Accuracy: {(correct/total)*100:.2f}%"
    )

    print("=" * 80)


if __name__ == "__main__":

    evaluate()