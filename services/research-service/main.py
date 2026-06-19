from fastapi import FastAPI
from app.routes.company import router

app = FastAPI()


@app.get("/health")
def health():
    return {
        "status": "running"
    }


app.include_router(router)