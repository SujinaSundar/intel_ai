from fastapi import FastAPI

app = FastAPI()


@app.get("/risk/{company}")
def risk(company: str):

    return {
        "company": company,
        "risk_score": 50
    }