"""Employee data access layer."""

import uuid
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

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
            stmt = stmt.where(Employee.job_title == job_title)
            count_stmt = count_stmt.where(Employee.job_title == job_title)

        total = self.db.scalar(count_stmt) or 0
        rows = (
            self.db.scalars(
                stmt.order_by(Employee.created_at.desc()).offset(offset).limit(limit)
            ).all()
        )
        return list(rows), total

    def update(self, employee: Employee, data: EmployeeUpdate) -> Employee:
        updates = data.model_dump(exclude_unset=True)
        if "country" in updates and updates["country"] is not None:
            updates["country"] = updates["country"].value
        for field, value in updates.items():
            setattr(employee, field, value)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def delete(self, employee: Employee) -> None:
        self.db.delete(employee)
        self.db.commit()

    def bulk_insert(self, rows: list[dict[str, Any]]) -> None:
        self.db.bulk_insert_mappings(Employee, rows)
        self.db.commit()
