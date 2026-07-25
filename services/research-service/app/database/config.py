from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

ENV_FILE = Path(".env")


class Settings(BaseSettings):
    """
    Application settings.
    """

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    MARKETAUX_API_KEY: str

    GROQ_API_KEY: str

    NEO4J_URI: str
    NEO4J_USERNAME: str
    NEO4J_PASSWORD: str
    
    CHROMA_DB_PATH: str = "chroma_db"

    CHROMA_COLLECTION_NAME: str = "financial_reports"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        extra="ignore",
    )


settings = Settings()