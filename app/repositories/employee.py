"""Employee repository."""

import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate


def _job_title_filter(term: str):
    """Partial, case-insensitive match (e.g. 'finance' → 'Financial Analyst')."""
    cleaned = term.strip()
    if not cleaned:
        return None

    patterns = {f"%{cleaned}%"}
    if len(cleaned) >= 4:
        # 'finance' also matches words starting with 'financ' (Financial, Finance)
        patterns.add(f"{cleaned[:-1]}%")
        patterns.add(f"% {cleaned}%")
        patterns.add(f"% {cleaned[:-1]}%")

    return or_(*[Employee.job_title.ilike(p) for p in patterns])


class EmployeeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, employee_id: uuid.UUID) -> Employee | None:
        return self.db.get(Employee, employee_id)

    def list_employees(
        self,
        *,
        country: str | None = None,
        job_title: str | None = None,
        offset: int = 0,
        limit: int = 50,
    ) -> tuple[list[Employee], int]:
        stmt = select(Employee)
        count_stmt = select(func.count()).select_from(Employee)

        if country:
            stmt = stmt.where(Employee.country == country)
            count_stmt = count_stmt.where(Employee.country == country)

        if job_title:
            title_filter = _job_title_filter(job_title)
            if title_filter is not None:
                stmt = stmt.where(title_filter)
                count_stmt = count_stmt.where(title_filter)

        total = self.db.scalar(count_stmt) or 0
        rows = self.db.scalars(
            stmt.order_by(Employee.created_at.desc()).offset(offset).limit(limit)
        ).all()
        return list(rows), total

    def create(self, data: EmployeeCreate) -> Employee:
        employee = Employee(
            id=uuid.uuid4(),
            full_name=data.full_name,
            job_title=data.job_title,
            country=data.country.value,
            salary=data.salary,
            currency=data.currency,
        )
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee
