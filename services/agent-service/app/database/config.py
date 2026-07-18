from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

# Optional local .env file.
# If it doesn't exist, Pydantic reads from OS environment variables.
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

    ALPHA_VANTAGE_API_KEY: str

    GROQ_API_KEY: str

    NEO4J_URI: str
    NEO4J_USERNAME: str
    NEO4J_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE) if ENV_FILE.exists() else None,
        extra="ignore",
    )


settings = Settings()