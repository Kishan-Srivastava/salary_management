"""Employee service."""

import uuid

from sqlalchemy.orm import Session

from app.repositories.employee import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate


class EmployeeNotFoundError(Exception):
    pass


class EmployeeService:
    def __init__(self, db: Session) -> None:
        self.repo = EmployeeRepository(db)

    def _require_employee(self, employee) -> EmployeeResponse:
        if not employee:
            raise EmployeeNotFoundError("Employee not found")
        return EmployeeResponse.model_validate(employee)

    def create(self, data: EmployeeCreate) -> EmployeeResponse:
        employee = self.repo.create(data)
        return EmployeeResponse.model_validate(employee)

    def get(self, employee_id: uuid.UUID) -> EmployeeResponse:
        return self._require_employee(self.repo.get_by_id(employee_id))

    def get_by_emp_id(self, emp_id: int) -> EmployeeResponse:
        return self._require_employee(self.repo.get_by_emp_id(emp_id))

    def list(
        self,
        *,
        country: str | None = None,
        job_title: str | None = None,
        name: str | None = None,
        emp_id: str | None = None,
        id_partial: str | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> tuple[list[EmployeeResponse], int]:
        offset = max(page - 1, 0) * page_size
        rows, total = self.repo.list_employees(
            country=country,
            job_title=job_title,
            name=name,
            emp_id=emp_id,
            id_partial=id_partial,
            offset=offset,
            limit=page_size,
        )
        return [EmployeeResponse.model_validate(row) for row in rows], total

    def update(self, employee_id: uuid.UUID, data: EmployeeUpdate) -> EmployeeResponse:
        employee = self.repo.get_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError(f"Employee {employee_id} not found")
        updated = self.repo.update(employee, data)
        return EmployeeResponse.model_validate(updated)

    def update_by_emp_id(self, emp_id: int, data: EmployeeUpdate) -> EmployeeResponse:
        employee = self.repo.get_by_emp_id(emp_id)
        if not employee:
            raise EmployeeNotFoundError(f"Employee emp_id {emp_id} not found")
        updated = self.repo.update(employee, data)
        return EmployeeResponse.model_validate(updated)

    def delete(self, employee_id: uuid.UUID) -> None:
        employee = self.repo.get_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError(f"Employee {employee_id} not found")
        self.repo.delete(employee)

    def delete_by_emp_id(self, emp_id: int) -> None:
        employee = self.repo.get_by_emp_id(emp_id)
        if not employee:
            raise EmployeeNotFoundError(f"Employee emp_id {emp_id} not found")
        self.repo.delete(employee)
