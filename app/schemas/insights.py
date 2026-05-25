"""Salary insights Pydantic schemas."""

from pydantic import BaseModel, Field


class CountrySalaryStats(BaseModel):
    country: str
    min_salary: float
    max_salary: float
    avg_salary: float
    employee_count: int


class JobTitleCountryStats(BaseModel):
    country: str
    job_title: str
    avg_salary: float
    employee_count: int


class SalaryBucket(BaseModel):
    bucket_label: str
    count: int


class SalaryDistribution(BaseModel):
    country: str | None = None
    buckets: list[SalaryBucket]


class TopJobRole(BaseModel):
    job_title: str
    avg_salary: float
    employee_count: int


class TopJobRolesByCountry(BaseModel):
    country: str
    roles: list[TopJobRole] = Field(default_factory=list)


class InsightsSummary(BaseModel):
    by_country: list[CountrySalaryStats]
    by_job_title_country: list[JobTitleCountryStats]
    salary_distribution: SalaryDistribution
    top_roles_by_country: list[TopJobRolesByCountry]
