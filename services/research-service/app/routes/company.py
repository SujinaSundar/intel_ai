from database.connection import SessionLocal
from database.models import Company
from fastapi import APIRouter

router = APIRouter()


@router.get("/companies")
def get_companies():

    db = SessionLocal()

    companies = db.query(
        Company
    ).all()

    return companies