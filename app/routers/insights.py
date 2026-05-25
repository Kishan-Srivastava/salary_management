"""Salary insights API routes."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.employee import Country
from app.schemas.insights import (
    CountrySalaryStats,
    JobTitleCountryStats,
    InsightsSummary,
    SalaryDistribution,
    TopJobRolesByCountry,
)
from app.services.insights import InsightsService

router = APIRouter()


def get_insights_service(db: Session = Depends(get_db)) -> InsightsService:
    return InsightsService(db)


@router.get("/country", response_model=list[CountrySalaryStats])
def insights_by_country(
    service: InsightsService = Depends(get_insights_service),
) -> list[CountrySalaryStats]:
    return service.country_insights()


@router.get("/job-title", response_model=list[JobTitleCountryStats])
def insights_by_job_title(
    service: InsightsService = Depends(get_insights_service),
) -> list[JobTitleCountryStats]:
    return service.job_title_insights()


@router.get("/distribution", response_model=SalaryDistribution)
def salary_distribution(
    country: Country | None = None,
    service: InsightsService = Depends(get_insights_service),
) -> SalaryDistribution:
    return service.salary_distribution(
        country=country.value if country else None
    )


@router.get("/top-roles", response_model=list[TopJobRolesByCountry])
def top_paying_roles(
    limit: int = Query(5, ge=1, le=20),
    service: InsightsService = Depends(get_insights_service),
) -> list[TopJobRolesByCountry]:
    return service.top_roles_by_country(limit=limit)


@router.get("/summary", response_model=InsightsSummary)
def insights_summary(
    country: Country | None = None,
    service: InsightsService = Depends(get_insights_service),
) -> InsightsSummary:
    return service.summary(country=country.value if country else None)
