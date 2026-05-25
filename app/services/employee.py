"""Employee service."""

import uuid

from sqlalchemy.orm import Session

from app.repositories.employee import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeResponse


class EmployeeNotFoundError(Exception):
    pass


class EmployeeService:
    def __init__(self, db: Session) -> None:
        self.repo = EmployeeRepository(db)

    def create(self, data: EmployeeCreate) -> EmployeeResponse:
        employee = self.repo.create(data)
        return EmployeeResponse.model_validate(employee)

    def get(self, employee_id: uuid.UUID) -> EmployeeResponse:
        employee = self.repo.get_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError(f"Employee {employee_id} not found")
        return EmployeeResponse.model_validate(employee)

    def list_all(self) -> list[EmployeeResponse]:
        rows = self.repo.list_all()
        return [EmployeeResponse.model_validate(row) for row in rows]
