from app.database.connection import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SELECT current_database();"))
    print(result.scalar())

    result = conn.execute(text("SELECT version();"))
    print(result.scalar())