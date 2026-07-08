"""
Evaluation engine.
"""

import json

from pathlib import Path

from app.rag.rag_pipeline import (
    ask_question
)

from app.rag.hybrid_rag_pipeline import (
    ask_hybrid_question
)

from app.evaluation.retrieval_metrics import (
    hit_rate,
    precision_at_k,
    recall_at_k,
    mean_reciprocal_rank,
    context_recall
)

from app.evaluation.generation_metrics import (
    semantic_similarity,
    answer_correctness
)


def load_benchmark() -> list[dict]:
    """
    Load benchmark questions.
    """

    benchmark_path = (
        Path(__file__)
        .parent
        / "benchmark.json"
    )

    with open(
        benchmark_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def evaluate_pipeline(
    pipeline_name: str,
    pipeline_function
) -> list[dict]:
    """
    Evaluate one pipeline.
    """

    benchmark = load_benchmark()

    results = []

    for sample in benchmark:

        question = sample["question"]

        company = sample.get(
            "company"
        )

        ground_truth = sample[
            "ground_truth"
        ]

        result = pipeline_function(

            question=question,

            company_name=company

        )

        answer = result["answer"]

        documents = result["documents"]

        metrics = {

            "pipeline": pipeline_name,

            "company": company,

            "question": question,

            "hit_rate": hit_rate(
                documents,
                ground_truth
            ),

            "precision@k": precision_at_k(
                documents,
                ground_truth
            ),

            "recall@k": recall_at_k(
                documents,
                ground_truth
            ),

            "mrr": mean_reciprocal_rank(
                documents,
                ground_truth
            ),

            "context_recall": context_recall(
                documents,
                ground_truth
            ),

            "semantic_similarity":
                semantic_similarity(
                    answer,
                    ground_truth
                ),

            "answer_correctness":
                answer_correctness(
                    answer,
                    ground_truth
                ),

            "retrieval_time":
                result["retrieval_time"]

        }

        results.append(
            metrics
        )

    return results


def evaluate_all() -> dict:
    """
    Evaluate all pipelines.
    """

    return {

        "Traditional RAG":
            evaluate_pipeline(
                "Traditional RAG",
                ask_question
            ),

        "Hybrid RAG":
            evaluate_pipeline(
                "Hybrid RAG",
                ask_hybrid_question
            )

    }