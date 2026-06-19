from fastapi import APIRouter

router = APIRouter(
    prefix="/news",
    tags=["News"]
)


@router.get("/{company}")
def get_news(company: str):

    return {
        "company": company,
        "news": [
            {
                "title": f"{company} announces new AI initiative",
                "source": "Economic Times"
            },
            {
                "title": f"{company} reports quarterly earnings",
                "source": "Moneycontrol"
            }
        ]
    }