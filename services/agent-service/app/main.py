from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.auth_router import router as auth_router
from app.router.agent import router


app = FastAPI(
    title="Agent Service"
)
@app.get("/debug")
def debug():
    return {
        "message": "THIS IS MY LOCAL UVICORN",
        "routes": [route.path for route in app.routes]
    }
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # tighten this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication Routes
app.include_router(auth_router)

# Agent Routes
app.include_router(router)

print("Registered routes:")
for route in app.routes:
    print(route.path)
@app.get("/")
def root():
    return {
        "service": "Agent Service",
        "status": "Running"
    }