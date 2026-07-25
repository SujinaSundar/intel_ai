# ETL Service Logging Documentation

## Overview

The ETL Service is responsible for ingesting stock and news data, performing sentiment analysis, and storing the processed information in PostgreSQL. Logging has been implemented across all ETL components to improve observability, debugging, and production monitoring.

---

# Logging Objectives

The logging implementation provides:

* End-to-end execution tracking
* Database operation monitoring
* External API monitoring
* Duplicate detection
* Data validation logging
* Exception tracing
* ETL execution summaries
* Consistent log format across all microservices

---

# Logging Architecture

```
Airflow DAG
      │
      ▼
Stock ETL Job
      │
      ▼
News ETL Job
      │
      ▼
Sentiment Worker
      │
      ▼
FinBERT Pipeline
      │
      ▼
PostgreSQL
```

All ETL components use the shared logger from:

```
app/core/logger.py
```

ensuring a consistent logging format across the project.

---

# Components Covered

## 1. Stock Data Ingestion

**File**

```
app/jobs/load_stock_data.py
```

### Logged Events

* ETL job started
* Number of companies retrieved
* Company currently being processed
* Yahoo Finance API request
* Number of stock records received
* Validation failures
* Duplicate stock records
* Records inserted
* Database commit
* Pipeline summary
* Exceptions
* Database session closed

---

## 2. News Data Ingestion

**File**

```
app/jobs/load_news_data.py
```

### Logged Events

* ETL job started
* Companies retrieved
* Marketaux API request
* Articles received
* Entity validation
* Missing field validation
* Duplicate article detection
* Articles stored
* Database commit
* Pipeline summary
* Exceptions
* Database session closed

---

## 3. Sentiment Pipeline

**File**

```
app/jobs/generate_sentiment.py
```

### Logged Events

* Pipeline started
* Database statistics
* Total articles
* Unprocessed articles
* News article processing
* Duplicate sentiment detection
* FinBERT prediction
* Sentiment storage
* Database commit
* Pipeline summary
* Exceptions
* Database session closed

---

## 4. Sentiment Worker

**File**

```
sentiment_worker.py
```

### Logged Events

* Worker started
* Polling interval
* Beginning polling cycle
* Sentiment processing completed
* Worker sleeping
* Unexpected exceptions

---

# Logging Levels

## INFO

Used for normal execution flow.

Examples

* ETL started
* Fetching stock data
* Fetching news
* Saving sentiment
* Pipeline completed

---

## WARNING

Used when execution continues but something unexpected occurs.

Examples

* Missing stock values
* Invalid publication date
* Empty API response
* Negative trading volume

---

## DEBUG

Used for detailed troubleshooting.

Examples

* Duplicate stock records
* Duplicate news articles
* Skipped records
* Validation failures

---

## EXCEPTION

Used whenever an exception occurs.

Example

```
logger.exception(
    "Stock ETL pipeline failed."
)
```

This automatically records the complete stack trace.

---

# ETL Summary Logs

Each ETL job generates a summary after successful execution.

### Stock ETL Summary

* Companies processed
* Stock records stored
* Execution completed

### News ETL Summary

* Companies processed
* Articles stored
* Execution completed

### Sentiment Summary

* Articles processed
* Articles skipped
* Total articles
* Pipeline completed

---

# Error Handling

Every ETL component follows the same exception handling pattern.

```
try:
    ...
except Exception:

    db.rollback()

    logger.exception(
        "Pipeline execution failed."
    )

    raise
```

This ensures:

* Database consistency
* Automatic rollback
* Full stack trace logging
* Error propagation

---

# Logging Benefits

The implemented logging provides:

* Improved debugging
* Faster issue diagnosis
* Better monitoring
* Production-ready observability
* Easier Airflow troubleshooting
* Consistent logging across all microservices
* Clear execution summaries
* Simplified maintenance

---

# ETL Logging Status

| Component           | Status    |
| ------------------- | --------- |
| Stock ETL           | Completed |
| News ETL            | Completed |
| Sentiment Pipeline  | Completed |
| Sentiment Worker    | Completed |
| Airflow Integration | Completed |

The ETL Service now follows a standardized logging strategy consistent with the Agent Service, Finance Service, and Research Service, providing complete traceability across the data ingestion and sentiment analysis pipeline.
