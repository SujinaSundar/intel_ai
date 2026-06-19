from app.database.connection import engine
from app.database.models import Base

print(Base.metadata.tables.keys())

Base.metadata.create_all(bind=engine)

print("Tables created")