"""Employee data access layer."""

import uuid

from sqlalchemy import select
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

    def list_all(self) -> list[Employee]:
        stmt = select(Employee).order_by(Employee.created_at.desc())
        return list(self.db.scalars(stmt).all())

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
