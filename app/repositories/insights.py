"""Salary insights repository — SQL aggregations."""

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.models.employee import Employee


class InsightsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def country_stats(self) -> list[dict]:
        stmt = (
            select(
                Employee.country,
                func.min(Employee.salary).label("min_salary"),
                func.max(Employee.salary).label("max_salary"),
                func.avg(Employee.salary).label("avg_salary"),
                func.count(Employee.id).label("employee_count"),
            )
            .group_by(Employee.country)
            .order_by(Employee.country)
        )
        rows = self.db.execute(stmt).mappings().all()
        return [dict(row) for row in rows]

    def job_title_country_stats(self) -> list[dict]:
        stmt = (
            select(
                Employee.country,
                Employee.job_title,
                func.avg(Employee.salary).label("avg_salary"),
                func.count(Employee.id).label("employee_count"),
            )
            .group_by(Employee.country, Employee.job_title)
            .order_by(Employee.country, Employee.job_title)
        )
        rows = self.db.execute(stmt).mappings().all()
        return [dict(row) for row in rows]

    def salary_distribution(self, country: str | None = None) -> list[dict]:
        labels = [
            "0k-50k",
            "50k-75k",
            "75k-100k",
            "100k-125k",
            "125k-150k",
            "150k-200k",
            ">=200k",
        ]
        bucket_case = case(
            (Employee.salary < 50000, labels[0]),
            (Employee.salary < 75000, labels[1]),
            (Employee.salary < 100000, labels[2]),
            (Employee.salary < 125000, labels[3]),
            (Employee.salary < 150000, labels[4]),
            (Employee.salary < 200000, labels[5]),
            else_=labels[6],
        )
        stmt = select(
            bucket_case.label("bucket_label"),
            func.count(Employee.id).label("count"),
        ).group_by(bucket_case)

        if country:
            stmt = stmt.where(Employee.country == country)

        rows = self.db.execute(stmt).mappings().all()
        return [dict(row) for row in rows]

    def top_job_roles_by_country(self, limit: int = 5) -> list[dict]:
        ranked = (
            select(
                Employee.country,
                Employee.job_title,
                func.avg(Employee.salary).label("avg_salary"),
                func.count(Employee.id).label("employee_count"),
                func.row_number()
                .over(
                    partition_by=Employee.country,
                    order_by=func.avg(Employee.salary).desc(),
                )
                .label("rank"),
            )
            .group_by(Employee.country, Employee.job_title)
        ).subquery()

        stmt = (
            select(ranked)
            .where(ranked.c.rank <= limit)
            .order_by(ranked.c.country, ranked.c.rank)
        )
        rows = self.db.execute(stmt).mappings().all()
        return [dict(row) for row in rows]
