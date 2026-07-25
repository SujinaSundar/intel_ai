from app.routes.company import router
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {
        "status": "running"
    }


app.include_router(router)