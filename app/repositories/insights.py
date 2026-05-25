"""Salary insights repository — SQL aggregations."""

from sqlalchemy import func, select
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
