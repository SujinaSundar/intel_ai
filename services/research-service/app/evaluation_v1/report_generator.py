"""
Generate evaluation report.
"""

from statistics import mean


def summarize(results: list[dict]) -> dict:
    """
    Compute average metrics.
    """

    return {

        "Hit Rate":
            mean(row["hit_rate"] for row in results),

        "Precision@k":
            mean(row["precision@k"] for row in results),

        "Recall@k":
            mean(row["recall@k"] for row in results),

        "MRR":
            mean(row["mrr"] for row in results),

        "Context Recall":
            mean(row["context_recall"] for row in results),

        "Semantic Similarity":
            mean(row["semantic_similarity"] for row in results),

        "Answer Correctness":
            mean(row["answer_correctness"] for row in results),

        "Retrieval Time":
            mean(row["retrieval_time"] for row in results)
    }


def print_report(
    evaluation_results: dict
) -> None:
    """
    Print evaluation report.
    """

    print()
    print("=" * 100)
    print("EVALUATION REPORT")
    print("=" * 100)

    for pipeline, results in evaluation_results.items():

        summary = summarize(results)

        print()
        print(pipeline)
        print("-" * 100)

        for metric, value in summary.items():

            print(
                f"{metric:<25}: {value:.4f}"
            )