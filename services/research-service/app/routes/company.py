from fastapi import APIRouter
from database.connection import SessionLocal
from database.models import Company

router = APIRouter()


@router.get("/companies")
def get_companies():

    db = SessionLocal()

    companies = db.query(
        Company
    ).all()

    return companies