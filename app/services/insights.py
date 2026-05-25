"""Salary insights business logic."""

from sqlalchemy.orm import Session

from app.repositories.insights import InsightsRepository
from app.schemas.insights import (
    CountrySalaryStats,
    JobTitleCountryStats,
    SalaryBucket,
    SalaryDistribution,
    TopJobRole,
    TopJobRolesByCountry,
)


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

    def job_title_insights(self) -> list[JobTitleCountryStats]:
        rows = self.repo.job_title_country_stats()
        return [
            JobTitleCountryStats(
                country=row["country"],
                job_title=row["job_title"],
                avg_salary=float(row["avg_salary"] or 0),
                employee_count=int(row["employee_count"]),
            )
            for row in rows
        ]

    def salary_distribution(self, country: str | None = None) -> SalaryDistribution:
        rows = self.repo.salary_distribution(country=country)
        return SalaryDistribution(
            country=country,
            buckets=[
                SalaryBucket(
                    bucket_label=row["bucket_label"],
                    count=int(row["count"]),
                )
                for row in rows
            ],
        )

    def top_roles_by_country(self, limit: int = 5) -> list[TopJobRolesByCountry]:
        rows = self.repo.top_job_roles_by_country(limit=limit)
        grouped: dict[str, list[TopJobRole]] = {}
        for row in rows:
            grouped.setdefault(row["country"], []).append(
                TopJobRole(
                    job_title=row["job_title"],
                    avg_salary=float(row["avg_salary"] or 0),
                    employee_count=int(row["employee_count"]),
                )
            )
        return [
            TopJobRolesByCountry(country=country, roles=roles)
            for country, roles in sorted(grouped.items())
        ]
