"""
Evaluation engine.
"""

from app.evaluation.benchmark_loader import (
    load_benchmark
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

from app.rag.rag_pipeline import (
    ask_question
)

from app.rag.hybrid_rag_pipeline import (
    ask_hybrid_question
)

from app.graph_rag.graph_rag_pipeline import (
    ask_graph_question
)

from app.hybrid_graph_rag.hybrid_graph_pipeline import (
    ask_hybrid_graph_question
)


def evaluate_pipeline(
    pipeline_name: str,
    pipeline_function
) -> list[dict]:
    """
    Evaluate one RAG pipeline.

    Parameters
    ----------
    pipeline_name : str

    pipeline_function

    Returns
    -------
    list[dict]
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

        print()

        print("=" * 100)

        print(
            f"Pipeline : {pipeline_name}"
        )

        print(
            f"Question : {question}"
        )

        print("=" * 100)

        # -----------------------------------
        # Execute Pipeline
        # -----------------------------------

        if pipeline_name == "Hybrid GraphRAG":

            result = pipeline_function(

                question=question

            )

        else:

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

            "ground_truth": ground_truth,

            "generated_answer": answer,

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

            ),

        "Graph RAG":

            evaluate_pipeline(

                "Graph RAG",

                ask_graph_question

            ),

        "Hybrid GraphRAG":

            evaluate_pipeline(

                "Hybrid GraphRAG",

                ask_hybrid_graph_question

            )

    }