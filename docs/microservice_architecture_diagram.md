                        Streamlit UI
                              |
                        API Gateway
                              |
 -----------------------------------------------------------------
 |                       |                    |                   |
 |                       |                    |                   |
Research Service     News Service      Risk Service      Agent Service
(FastAPI)            (FastAPI)         (FastAPI)         (LangGraph)
 |                       |                    |                   |
 -----------------------------------------------------------------
                              |
                      Shared Data Layer
                              |
 ---------------------------------------------------------
 |                       |                              |
PostgreSQL           ChromaDB                        Neo4j
                              |
                        ETL Service
                         (Airflow)