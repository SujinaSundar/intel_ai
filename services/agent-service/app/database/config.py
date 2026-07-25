"""
Application configuration.

Loads environment variables
from a local .env file
(if available) or from
the operating system
environment variables.
"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

# -----------------------------------------------------
# Environment File
# -----------------------------------------------------

ENV_FILE = Path(".env")


class Settings(BaseSettings):
    """
    Application settings.

    Configuration values are
    loaded from the local
    .env file (if present)
    or from environment
    variables.
    """

    # -------------------------------------------------
    # PostgreSQL
    # -------------------------------------------------

    POSTGRES_HOST: str

    POSTGRES_PORT: int = 5432

    POSTGRES_DB: str

    POSTGRES_USER: str

    POSTGRES_PASSWORD: str

    # -------------------------------------------------
    # External APIs
    # -------------------------------------------------

    MARKETAUX_API_KEY: str
    
    GROQ_API_KEY: str

    # -------------------------------------------------
    # Neo4j
    # -------------------------------------------------

    NEO4J_URI: str

    NEO4J_USERNAME: str

    NEO4J_PASSWORD: str

    # -------------------------------------------------
    # Microservices
    # -------------------------------------------------

    RESEARCH_SERVICE_URL: str

    # -------------------------------------------------
    # JWT
    # -------------------------------------------------

    JWT_SECRET_KEY: str = Field(
        min_length=32,
    )

    JWT_ALGORITHM: str = "HS256"

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # -------------------------------------------------
    # Pydantic Configuration
    # -------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE) if ENV_FILE.exists() else None,
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
    )

    # -------------------------------------------------
    # Helper Properties
    # -------------------------------------------------

    @property
    def postgres_url(self) -> str:
        """
        SQLAlchemy database URL.
        """

        return (
            f"postgresql://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )


settings = Settings()