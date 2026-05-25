"""Step 9 — seed script tests."""

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.employee import Employee
from scripts.seed import build_employees, seed


def test_build_employees_count() -> None:
    employees = build_employees(10)
    assert len(employees) == 10
    assert all(e.full_name for e in employees)
    assert all(e.salary > 0 for e in employees)


def test_seed_inserts_into_database() -> None:
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
