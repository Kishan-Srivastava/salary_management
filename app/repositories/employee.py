"""Employee repository — Step 2: create only."""

import uuid

from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate


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
