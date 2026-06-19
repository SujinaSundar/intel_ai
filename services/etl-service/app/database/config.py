from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

DOCKER_ENV = Path("/opt/airflow/.env")
LOCAL_ENV = Path(__file__).resolve().parents[4] / ".env"

ENV_FILE = DOCKER_ENV if DOCKER_ENV.exists() else LOCAL_ENV

class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    ALPHA_VANTAGE_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        extra="ignore"
    )

settings = Settings()