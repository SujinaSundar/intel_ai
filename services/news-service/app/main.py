from app.routes.news import router as news_router
from fastapi import FastAPI

app = FastAPI(
    title="News Service",
    version="1.0.0"
)

@app.get("/health")
def health():
    return {
        "status": "running",
        "service": "news-service"
    }

app.include_router(news_router)