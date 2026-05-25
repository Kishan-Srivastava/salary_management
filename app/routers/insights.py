"""Salary insights routes — Step 7: country stats."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.insights import CountrySalaryStats
from app.services.insights import InsightsService

router = APIRouter()


def get_insights_service(db: Session = Depends(get_db)) -> InsightsService:
    return InsightsService(db)


@router.get("/country", response_model=list[CountrySalaryStats])
def insights_by_country(
    service: InsightsService = Depends(get_insights_service),
) -> list[CountrySalaryStats]:
    return service.country_insights()
