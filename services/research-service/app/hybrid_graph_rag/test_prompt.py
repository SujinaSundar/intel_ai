from app.hybrid_graph_rag.hybrid_graph_prompt import (
    build_hybrid_graph_prompt
)


prompt = build_hybrid_graph_prompt(

    question=
    "What does HDFC Bank focus on?",

    documents=[
        "HDFC Bank annual report..."
    ],

    graph_documents=[
        "HDFC Bank FOCUSES_ON Banking"
    ],

    sentiment_text=
    "Positive",

    stock_text=
    "Close Price: 2100"
)

print(prompt[:1000])