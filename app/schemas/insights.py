"""Insights API schemas — Step 7: country stats."""

from pydantic import BaseModel


class CountrySalaryStats(BaseModel):
    country: str
    min_salary: float
    max_salary: float
    avg_salary: float
    employee_count: int
