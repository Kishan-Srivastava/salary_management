"""Step 9–10 — seed script tests."""

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.employee import Employee
from app.repositories.employee import EmployeeRepository
from scripts.seed import BATCH_SIZE, build_employee_rows, seed


def test_build_employee_rows() -> None:
    rows = build_employee_rows(10)
    assert len(rows) == 10
    assert all(row["full_name"] for row in rows)
    assert all(row["salary"] > 0 for row in rows)
    assert "id" in rows[0]
    assert rows[0]["emp_id"] == 1
    assert rows[-1]["emp_id"] == 10


def test_seed_inserts_via_bulk_insert() -> None:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    session_factory = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = session_factory()

    seed(db, 5)
    total = db.scalar(select(func.count()).select_from(Employee))
    assert total == 5
    db.close()


def test_bulk_insert_batch_size() -> None:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    session_factory = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = session_factory()
    repo = EmployeeRepository(db)

    rows = build_employee_rows(BATCH_SIZE + 100)
    seed(db, len(rows))
    total = db.scalar(select(func.count()).select_from(Employee))
    assert total == BATCH_SIZE + 100
    db.close()
