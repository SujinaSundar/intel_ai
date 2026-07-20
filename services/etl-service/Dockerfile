FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Copy dependency files from the project root
COPY pyproject.toml ./
COPY uv.lock ./

# Install dependencies
RUN uv sync --frozen

# Copy the entire repository
COPY . .

# Run from the ETL service directory
WORKDIR /app/services/etl-service

CMD ["uv", "run", "python", "-m", "app.jobs.sentiment_worker"]