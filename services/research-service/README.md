# Research Service Documentation

## Overview

The Research Service is responsible for answering company research questions using a Hybrid GraphRAG architecture. It combines structured graph knowledge stored in Neo4j with semantic document retrieval from PostgreSQL/ChromaDB to generate context-aware responses using an LLM.

The service is independent of the Agent Service and exposes REST APIs for research-related queries.

---

# Responsibilities

The Research Service performs the following tasks:

- Retrieve company information
- Search annual report document chunks
- Query Neo4j knowledge graph
- Build Hybrid GraphRAG context
- Retrieve related sentiment information
- Retrieve stock information
- Generate LLM responses
- Return structured research answers

---

# Research Architecture

```text
                    User Query
                         │
                         ▼
                Research API Endpoint
                         │
                         ▼
                Research Service
                         │
         ┌───────────────┼────────────────┐
         │               │                │
         ▼               ▼                ▼
   PostgreSQL       Neo4j Graph      ChromaDB
(Document Chunks)   Relationships   Vector Search
         │               │                │
         └───────────────┼────────────────┘
                         ▼
               Hybrid Context Builder
                         │
                         ▼
                    Groq LLM
                         │
                         ▼
                 Research Response
```

---

# Service Components

## 1. REST API

Provides research endpoints for the Agent Service.

Responsibilities

- Receive research requests
- Validate input
- Invoke research pipeline
- Return structured responses

---

## 2. Hybrid Context Builder

Builds context from multiple data sources.

Sources

- PostgreSQL document chunks
- Neo4j knowledge graph
- Sentiment scores
- Stock information

Responsibilities

- Retrieve relevant documents
- Retrieve graph relationships
- Merge contexts
- Build final prompt context

---

## 3. GraphRAG

GraphRAG enhances traditional RAG by combining semantic retrieval with graph traversal.

Responsibilities

- Query Neo4j
- Retrieve related entities
- Retrieve company relationships
- Expand research context

---

## 4. LLM Layer

Uses Groq Llama 3.3 70B.

Responsibilities

- Receive Hybrid GraphRAG context
- Generate research answer
- Produce natural language response

---

# Research Workflow

```text
User Question
      │
      ▼
Research Endpoint
      │
      ▼
Company Validation
      │
      ▼
Hybrid Context Builder
      │
      ├────────► PostgreSQL
      │
      ├────────► Neo4j
      │
      ├────────► Sentiment
      │
      └────────► Stock Data
      │
      ▼
Groq LLM
      │
      ▼
Research Response
```

---

# Logging Strategy

The Research Service implements structured logging across all layers.

---

## API Layer

Logs

- Request received
- Company name
- User question
- Response generated
- Exceptions

---

## Database Layer

Logs

- PostgreSQL connection
- Document retrieval
- Number of chunks retrieved
- Database errors

---

## Graph Layer

Logs

- Neo4j connection
- Graph query execution
- Relationships retrieved
- Graph traversal errors

---

## Hybrid Context Builder

Logs

- Context building started
- Documents retrieved
- Graph nodes retrieved
- Sentiment retrieved
- Stock data retrieved
- Context completed

---

## LLM Layer

Logs

- Prompt generation
- LLM request
- Response received
- Token usage (if available)
- LLM exceptions

---

# Logging Levels

## INFO

Normal execution

Examples

- Research started
- Company found
- Documents retrieved
- Graph retrieved
- LLM response generated

---

## WARNING

Unexpected but recoverable events

Examples

- Company not found
- No graph relationships
- No document chunks

---

## DEBUG

Detailed execution

Examples

- Retrieved document IDs
- Graph node IDs
- Context size
- Prompt construction

---

## EXCEPTION

Unexpected failures

Example

```python
logger.exception(
    "Research pipeline failed."
)
```

---

# Error Handling

All components follow a common exception pattern.

```python
try:
    ...

except Exception:

    logger.exception(
        "Research execution failed."
    )

    raise
```

This ensures

- Complete stack trace
- Easier debugging
- Consistent logging
- Error propagation

---

# Research Pipeline

The research pipeline performs the following sequence.

1. Receive question
2. Validate company
3. Retrieve document chunks
4. Retrieve graph relationships
5. Retrieve sentiment
6. Retrieve stock information
7. Build Hybrid GraphRAG context
8. Send prompt to Groq
9. Generate response
10. Return answer

---

# Data Sources

## PostgreSQL

Stores

- Companies
- Research reports
- Document chunks
- News metadata
- Sentiment scores
- Stock prices

---

## Neo4j

Stores

- Company nodes
- Entity nodes
- Financial relationships
- Graph connections

---

## ChromaDB

Stores

- Vector embeddings
- Semantic document index

---

# APIs

Example endpoint

```
POST /research/ask
```

Example request

```json
{
    "company": "Infosys",
    "question": "Should I invest in Infosys?"
}
```

Example response

```json
{
    "success": true,
    "answer": "...generated research response..."
}
```

---

# Logging Benefits

The logging implementation provides

- Complete request tracing
- Database visibility
- Graph query monitoring
- LLM request tracking
- Easier debugging
- Production monitoring
- Faster issue diagnosis

---

# Research Service Status

| Component | Status |
|------------|--------|
| REST API | Completed |
| PostgreSQL Integration | Completed |
| Neo4j Integration | Completed |
| GraphRAG | Completed |
| Hybrid Context Builder | Completed |
| LLM Integration | Completed |
| Structured Logging | Completed |

The Research Service now implements a production-ready Hybrid GraphRAG architecture with structured logging, enabling efficient retrieval of financial documents, graph relationships, and sentiment information to generate comprehensive research responses.