"""Employee service — Step 2: create only."""

from sqlalchemy.orm import Session

from app.repositories.employee import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeResponse


class EmployeeService:
    def __init__(self, db: Session) -> None:
        self.repo = EmployeeRepository(db)

    def create(self, data: EmployeeCreate) -> EmployeeResponse:
        employee = self.repo.create(data)
        return EmployeeResponse.model_validate(employee)
