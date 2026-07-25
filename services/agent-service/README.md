# 🤖 Agent Service

## AI-Powered Trading Research Orchestration Service

---

# Overview

The **Agent Service** is the orchestration layer of the **NIFTY 50 Trading Research Agent** platform. It exposes REST APIs to clients, authenticates users using JWT, coordinates multiple AI agents through a LangGraph workflow, communicates with downstream microservices via the Model Context Protocol (MCP), and generates a unified natural-language response.

Unlike a traditional chatbot, the Agent Service does not contain all business logic itself. Instead, it acts as an intelligent controller that determines which specialized agent should answer a user's query and aggregates the results into a coherent response.

---

# Responsibilities

The Agent Service is responsible for:

* Exposing REST APIs
* JWT Authentication
* User Authorization
* LangGraph Workflow Execution
* AI Supervisor Routing
* Invoking Specialized Agents
* MCP Communication
* Response Generation
* Logging
* Exception Handling

---

# Features

* FastAPI REST API
* JWT Authentication
* LangGraph-based Agent Workflow
* AI Supervisor Agent
* Finance Agent
* News Agent
* Research Agent
* Comparison Agent
* Sector Agent
* MCP-based Microservice Communication
* Structured Logging
* Global Exception Handling
* Request Logging Middleware
* Modular Architecture
* Docker Support

---

# High-Level Architecture

```
                    Client / Frontend
                            │
                            ▼
                    FastAPI REST API
                            │
                            ▼
                    Authentication Layer
                            │
                            ▼
                      Chat Service
                            │
                            ▼
                 LangGraph Workflow Runner
                            │
                            ▼
                    Supervisor Agent
                            │
      ┌───────────┬──────────┬────────────┬────────────┐
      ▼           ▼          ▼            ▼            ▼
 Finance       News      Research    Comparison    Sector
  Agent        Agent       Agent        Agent       Agent
      │           │           │            │            │
      ▼           ▼           ▼            ▼            ▼
 Finance MCP  News MCP  Research MCP Comparison MCP Sector MCP
      │           │           │            │            │
      ▼           ▼           ▼            ▼            ▼
 Individual Backend Microservices
                            │
                            ▼
                   Response Generator
                            │
                            ▼
                     Final AI Response
```

---

# Technology Stack

| Component        | Technology           |
| ---------------- | -------------------- |
| Language         | Python 3.12          |
| Framework        | FastAPI              |
| Workflow         | LangGraph            |
| LLM              | Groq (Llama 3.3 70B) |
| Authentication   | JWT                  |
| Database         | PostgreSQL           |
| Communication    | MCP                  |
| Validation       | Pydantic             |
| Logging          | Python Logging       |
| Containerization | Docker               |

---

# Project Structure

```
agent-service/

├── app/
│   ├── agents/
│   ├── auth/
│   ├── core/
│   ├── database/
│   ├── exceptions/
│   ├── langgraph/
│   ├── llm/
│   ├── mcp/
│   ├── prompts/
│   ├── response/
│   ├── router/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── create_tables.py
├── Dockerfile
└── README.md
```

---

# Request Lifecycle

```
User

↓

POST /ask

↓

JWT Authentication

↓

Chat Service

↓

Workflow Runner

↓

Supervisor Agent

↓

Route Selection

↓

Selected Agent

↓

MCP Client

↓

Backend Service

↓

Response Generator

↓

Final Response
```

---

# LangGraph Workflow

The Agent Service uses **LangGraph** to orchestrate every request.

The workflow consists of several independent nodes.

## 1. Router Node

The Router Node invokes the Supervisor Agent to classify the user's intent and determine which specialized agent should handle the request.

Possible routes include:

* Finance
* News
* Research
* Comparison
* Sector

---

## 2. Finance Node

Handles:

* Latest Stock Price
* Historical Prices
* Trading Volume
* Stock Summary

Communicates with the Finance Service through Finance MCP.

---

## 3. News Node

Handles:

* Latest News
* Company News
* News Sentiment

Communicates with the News Service.

---

## 4. Research Node

Handles:

* Annual Reports
* Financial Analysis
* GraphRAG Queries
* Hybrid RAG

Communicates with the Research Service.

---

## 5. Comparison Node

Handles:

* Company Comparison
* Stock Comparison
* Financial Metrics Comparison

---

## 6. Sector Node

Handles:

* Sector Analysis
* Industry Trends
* Sector Performance

---

## 7. Response Node

The Response Generator converts structured outputs from specialized agents into a single natural-language response suitable for the user.

---

# Supervisor Agent

The Supervisor Agent acts as the intelligent router.

Responsibilities include:

* Intent Classification
* Entity Extraction
* Company Identification
* Sector Identification
* Route Selection

The Supervisor does not answer questions directly; it decides which specialized agent should process the request.

---

# Specialized Agents

## Finance Agent

Handles market data queries.

Examples:

* Current Price
* Price History
* Trading Volume

---

## News Agent

Handles company news retrieval and sentiment analysis.

---

## Research Agent

Handles document-based queries using GraphRAG and Hybrid RAG.

---

## Comparison Agent

Compares multiple companies using financial and research data.

---

## Sector Agent

Answers questions about industries and market sectors.

---

# MCP Communication

Instead of directly querying databases, the Agent Service communicates with downstream services using the Model Context Protocol (MCP).

Benefits include:

* Loose Coupling
* Better Scalability
* Independent Deployments
* Easier Maintenance
* Service Isolation

---

# Authentication

Authentication is implemented using JWT.

Workflow:

1. User Login
2. JWT Generation
3. Token Validation
4. Protected Endpoint Access

Protected Endpoint:

```
POST /ask
```

Authentication Header:

```
Authorization: Bearer <JWT_TOKEN>
```

---

# Logging

The Agent Service implements structured logging across all layers.

Logging includes:

* Application Startup
* Request Processing
* Agent Routing
* Workflow Execution
* Errors
* Warnings
* Shutdown Events

---

# Exception Handling

Centralized exception handling provides consistent API responses.

Handled exceptions include:

* Invalid Requests
* Authentication Errors
* Validation Errors
* Internal Server Errors
* MCP Communication Failures

---

# REST API

## Health Check

```
GET /
```

Returns:

```json
{
  "service": "Agent Service",
  "status": "Running"
}
```

---

## Debug

```
GET /debug
```

Returns all registered routes for development.

---

## Ask AI

```
POST /ask
```

Authentication Required:

Yes

Example Request

```json
{
  "question": "Compare Infosys and TCS"
}
```

Example Response

```json
{
  "answer": "..."
}
```

---

# Environment Variables

Example:

```env
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=

NEO4J_URI=
NEO4J_USERNAME=
NEO4J_PASSWORD=

GROQ_API_KEY=

JWT_SECRET_KEY=
JWT_ALGORITHM=

RESEARCH_SERVICE_URL=
```

---

# Running Locally

```bash
uv sync

uv run uvicorn app.main:app --reload --port 8000
```

---

# Docker

Build

```bash
docker build -t intel-ai-agent .
```

Run

```bash
docker run -p 8000:8000 intel-ai-agent
```

---

# Testing

Example:

```bash
pytest
```

Recommended test coverage:

* Agent Routing
* Supervisor Logic
* Finance Agent
* News Agent
* Research Agent
* Comparison Agent
* Sector Agent
* Workflow Execution
* Response Generator
* Authentication
* API Endpoints

---

# Future Enhancements

* Conversation Memory
* Multi-turn Dialogue
* Streaming Responses
* Agent Caching
* Tool Calling
* Observability Dashboard
* Distributed Tracing
* Rate Limiting
* RBAC
* Agent Evaluation Framework

---

# Key Highlights

* Microservice-based Architecture
* LangGraph Agent Orchestration
* AI Supervisor Routing
* MCP Communication Layer
* JWT Authentication
* Modular Design
* Production-ready Logging
* Global Exception Handling
* Dockerized Deployment
* Extensible Agent Framework

---

# Conclusion

The Agent Service serves as the intelligent orchestration layer of the NIFTY 50 Trading Research platform. By combining FastAPI, LangGraph, JWT authentication, specialized AI agents, and MCP-based communication, it provides a scalable and maintainable architecture capable of answering diverse financial research queries through a unified API while remaining loosely coupled with downstream microservices.
