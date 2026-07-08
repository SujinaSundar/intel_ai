"""
Generate evaluation report.
"""

from statistics import mean

import pandas as pd


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
    Print and save evaluation report.
    """

    summary_rows = []

    detailed_rows = []

    print()

    print("=" * 120)

    print("EVALUATION REPORT")

    print("=" * 120)

    for pipeline, results in evaluation_results.items():

        summary = summarize(results)

        summary_rows.append({

            "Pipeline": pipeline,

            **summary

        })

        detailed_rows.extend(results)

        print()

        print(pipeline)

        print("-" * 120)

        for metric, value in summary.items():

            print(

                f"{metric:<25}: {value:.4f}"

            )

    summary_df = pd.DataFrame(
        summary_rows
    )

    detail_df = pd.DataFrame(
        detailed_rows
    )

    summary_df.to_csv(

        "evaluation_summary.csv",

        index=False

    )

    detail_df.to_csv(

        "evaluation_results.csv",

        index=False

    )

    print()

    print("Saved evaluation_summary.csv")

    print("Saved evaluation_results.csv")