from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.config import settings
from urllib.parse import quote_plus

password = quote_plus(settings.POSTGRES_PASSWORD)

DATABASE_URL = (
    f"postgresql://{settings.POSTGRES_USER}:{password}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)
print(DATABASE_URL)
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

print("HOST =", settings.POSTGRES_HOST)
print(DATABASE_URL)