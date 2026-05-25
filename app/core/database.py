"""Database engine and session."""

from collections.abc import Generator

from sqlalchemy import create_engine, event, inspect, select, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


def _build_engine(url: str):
    connect_args: dict = {}
    if url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    engine = create_engine(url, connect_args=connect_args)

    if url.startswith("sqlite"):

        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record) -> None:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


settings = get_settings()
engine = _build_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _migrate_emp_id_column() -> None:
    """Add emp_id to existing SQLite DBs and backfill unique integers."""
    from app.models.employee import Employee
    from app.repositories.employee import EmployeeRepository

    inspector = inspect(engine)
    if "employees" not in inspector.get_table_names():
        return

    columns = {col["name"] for col in inspector.get_columns("employees")}
    if "emp_id" not in columns:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE employees ADD COLUMN emp_id INTEGER"))

    db = SessionLocal()
    try:
        repo = EmployeeRepository(db)
        missing = list(
            db.scalars(
                select(Employee)
                .where(Employee.emp_id.is_(None))
                .order_by(Employee.created_at)
            ).all()
        )
        if not missing:
            return

        next_id = repo.next_emp_id()
        for employee in missing:
            employee.emp_id = next_id
            next_id += 1
        db.commit()
    finally:
        db.close()


def init_db() -> None:
    from app.models.employee import Employee  # noqa: F401

    Base.metadata.create_all(bind=engine)
    _migrate_emp_id_column()
