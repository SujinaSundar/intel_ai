"""
Evaluation visualization.
"""

import pandas as pd

import matplotlib.pyplot as plt


def plot_results(
    csv_file: str = "evaluation_summary.csv"
) -> None:
    """
    Plot evaluation metrics.
    """

    dataframe = pd.read_csv(
        csv_file
    )

    metrics = [

        "Hit Rate",

        "Precision@k",

        "Recall@k",

        "MRR",

        "Context Recall",

        "Semantic Similarity",

        "Answer Correctness",

        "Retrieval Time"

    ]

    for metric in metrics:

        plt.figure(
            figsize=(8, 5)
        )

        plt.bar(

            dataframe["Pipeline"],

            dataframe[metric]

        )

        plt.title(metric)

        plt.ylabel(metric)

        plt.tight_layout()

        plt.savefig(

            f"{metric.replace('@', '_').replace(' ', '_')}.png"

        )

        plt.close()

    print(
        "Evaluation plots generated."
    )