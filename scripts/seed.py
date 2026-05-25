"""Seed employees — Step 10: bulk insert for large datasets."""

from __future__ import annotations

import argparse
import random
import uuid
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.database import SessionLocal, init_db
from app.repositories.employee import EmployeeRepository

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
BATCH_SIZE = 1000

JOB_TITLES = [
    "Software Engineer",
    "Senior Software Engineer",
    "Staff Engineer",
    "Data Analyst",
    "Data Scientist",
    "Financial Analyst",
    "Product Manager",
    "Project Manager",
    "HR Manager",
    "Marketing Manager",
    "UX Designer",
    "DevOps Engineer",
    "QA Engineer",
]

COUNTRIES = ["US", "UK", "DE", "IN", "CA", "AU", "FR", "JP", "SG", "BR"]

COUNTRY_CURRENCY = {
    "US": "USD",
    "UK": "GBP",
    "DE": "EUR",
    "IN": "INR",
    "CA": "CAD",
    "AU": "AUD",
    "FR": "EUR",
    "JP": "JPY",
    "SG": "SGD",
    "BR": "BRL",
}

SALARY_RANGES: dict[str, tuple[int, int]] = {
    "Software Engineer": (70000, 130000),
    "Senior Software Engineer": (110000, 180000),
    "Staff Engineer": (150000, 220000),
    "Data Analyst": (55000, 95000),
    "Data Scientist": (90000, 160000),
    "Financial Analyst": (60000, 105000),
    "Product Manager": (100000, 170000),
    "Project Manager": (85000, 140000),
    "HR Manager": (65000, 110000),
    "Marketing Manager": (70000, 130000),
    "UX Designer": (65000, 115000),
    "DevOps Engineer": (90000, 155000),
    "QA Engineer": (55000, 100000),
}

COUNTRY_MULTIPLIER = {
    "US": 1.0,
    "UK": 0.85,
    "DE": 0.9,
    "IN": 0.35,
    "CA": 0.92,
    "AU": 0.88,
    "FR": 0.87,
    "JP": 0.8,
    "SG": 0.95,
    "BR": 0.45,
}


def load_names(filename: str) -> list[str]:
    path = DATA_DIR / filename
    with path.open(encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def build_employee_rows(count: int, start_emp_id: int = 1) -> list[dict]:
    first_names = load_names("first_names.txt")
    last_names = load_names("last_names.txt")
    now = datetime.now(timezone.utc)
    rows: list[dict] = []

    for offset in range(count):
        job_title = random.choice(JOB_TITLES)
        country = random.choice(COUNTRIES)
        low, high = SALARY_RANGES[job_title]
        salary = round(random.uniform(low, high) * COUNTRY_MULTIPLIER[country], 2)
        rows.append(
            {
                "id": uuid.uuid4(),
                "emp_id": start_emp_id + offset,
                "full_name": f"{random.choice(first_names)} {random.choice(last_names)}",
                "job_title": job_title,
                "country": country,
                "salary": salary,
                "currency": COUNTRY_CURRENCY[country],
                "created_at": now,
                "updated_at": now,
            }
        )
    return rows


def seed(db: Session, count: int) -> None:
    repo = EmployeeRepository(db)
    rows = build_employee_rows(count, start_emp_id=repo.next_emp_id())
    for start in range(0, len(rows), BATCH_SIZE):
        repo.bulk_insert(rows[start : start + BATCH_SIZE])


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed employee data")
    parser.add_argument(
        "--count",
        type=int,
        default=10_000,
        help="Number of rows (default 10000)",
    )
    args = parser.parse_args()

    init_db()
    db = SessionLocal()
    try:
        seed(db, args.count)
        print(f"Seeded {args.count} employees in batches of {BATCH_SIZE}.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
