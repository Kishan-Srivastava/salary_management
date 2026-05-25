"""Employee repository."""

import uuid
from typing import Any

from sqlalchemy import String, cast, func, or_, select
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def _name_filter(column, term: str):
    """Strict name match: substring or word start only (no stem truncation)."""
    search = term.strip().lower()
    if not search:
        return None

    lowered = func.lower(column)
    return or_(
        lowered.like(f"%{search}%"),
        lowered.like(f"{search}%"),
        lowered.like(f"% {search}%"),
    )


def _job_title_filter(column, term: str):
    """Job title match: substring/word start; optional stem for titles like finance → financial."""
    search = term.strip().lower()
    if not search:
        return None

    lowered = func.lower(column)
    clauses = [
        lowered.like(f"%{search}%"),
        lowered.like(f"{search}%"),
        lowered.like(f"% {search}%"),
    ]
    if len(search) >= 5:
        root = search[:-1]
        clauses.append(lowered.like(f"%{root}%"))
        clauses.append(lowered.like(f"% {root}%"))

    return or_(*clauses)


def _emp_id_partial_filter(term: str):
    search = term.strip()
    if not search:
        return None
    return cast(Employee.emp_id, String).like(f"%{search}%")


def _uuid_partial_filter(term: str):
    search = term.strip().lower()
    if not search:
        return None
    return func.lower(cast(Employee.id, String)).like(f"%{search}%")


class EmployeeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def next_emp_id(self) -> int:
        current = self.db.scalar(select(func.max(Employee.emp_id))) or 0
        return current + 1

    def get_by_id(self, employee_id: uuid.UUID) -> Employee | None:
        return self.db.get(Employee, employee_id)

    def get_by_emp_id(self, emp_id: int) -> Employee | None:
        return self.db.scalar(select(Employee).where(Employee.emp_id == emp_id))

    def list_employees(
        self,
        *,
        country: str | None = None,
        job_title: str | None = None,
        name: str | None = None,
        emp_id: str | None = None,
        id_partial: str | None = None,
        offset: int = 0,
        limit: int = 50,
    ) -> tuple[list[Employee], int]:
        stmt = select(Employee)
        count_stmt = select(func.count()).select_from(Employee)

        filters = []

        if country:
            filters.append(Employee.country == country)
        if job_title:
            title_filter = _job_title_filter(Employee.job_title, job_title)
            if title_filter is not None:
                filters.append(title_filter)
        if name:
            name_filter = _name_filter(Employee.full_name, name)
            if name_filter is not None:
                filters.append(name_filter)
        if emp_id:
            emp_filter = _emp_id_partial_filter(emp_id)
            if emp_filter is not None:
                filters.append(emp_filter)
        if id_partial:
            uuid_filter = _uuid_partial_filter(id_partial)
            if uuid_filter is not None:
                filters.append(uuid_filter)

        for condition in filters:
            stmt = stmt.where(condition)
            count_stmt = count_stmt.where(condition)

        total = self.db.scalar(count_stmt) or 0
        rows = self.db.scalars(
            stmt.order_by(Employee.emp_id.desc()).offset(offset).limit(limit)
        ).all()
        return list(rows), total

    def create(self, data: EmployeeCreate) -> Employee:
        employee = Employee(
            id=uuid.uuid4(),
            emp_id=self.next_emp_id(),
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
