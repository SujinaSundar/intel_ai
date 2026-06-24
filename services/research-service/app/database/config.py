from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


ENV_FILE = (
    Path(__file__).resolve().parents[4]
    / ".env"
)

print(
    "ENV FILE:",
    ENV_FILE
)

print(
    "EXISTS:",
    ENV_FILE.exists()
)


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
        env_file=str(ENV_FILE),
        extra="ignore"
    )


settings = Settings()

print(
    "HOST =",
    settings.POSTGRES_HOST
)

print(
    "PORT =",
    settings.POSTGRES_PORT
)