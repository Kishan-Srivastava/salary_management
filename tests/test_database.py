"""Step 1 — database and Employee model tests."""

import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.employee import Employee


def test_employee_table_exists(db_session: Session) -> None:
    employee = Employee(
        id=uuid.uuid4(),
        emp_id=1,
        full_name="Jane Doe",
        job_title="Engineer",
        country="US",
        salary=90000.00,
        currency="USD",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db_session.add(employee)
    db_session.commit()

    row = db_session.scalar(select(Employee).where(Employee.full_name == "Jane Doe"))
    assert row is not None
    assert row.country == "US"
    assert float(row.salary) == 90000.00


def test_employee_has_indexes() -> None:
    index_names = {index.name for index in Employee.__table__.indexes}
    assert "ix_employees_country" in index_names
    assert "ix_employees_job_title" in index_names
    assert "ix_employees_emp_id" in index_names
