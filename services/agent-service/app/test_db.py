from app.database.connection import SessionLocal

db = SessionLocal()

print("Database Connected Successfully!")

db.close()