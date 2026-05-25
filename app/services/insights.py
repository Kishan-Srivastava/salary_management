"""Salary insights business logic."""

from sqlalchemy.orm import Session

from app.repositories.insights import InsightsRepository
from app.schemas.insights import CountrySalaryStats


class InsightsService:
    def __init__(self, db: Session) -> None:
        self.repo = InsightsRepository(db)

    def country_insights(self) -> list[CountrySalaryStats]:
        rows = self.repo.country_stats()
        return [
            CountrySalaryStats(
                country=row["country"],
                min_salary=float(row["min_salary"] or 0),
                max_salary=float(row["max_salary"] or 0),
                avg_salary=float(row["avg_salary"] or 0),
                employee_count=int(row["employee_count"]),
            )
            for row in rows
        ]
