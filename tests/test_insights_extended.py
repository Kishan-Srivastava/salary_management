"""Step 8 — job-title insights, distribution, top roles (TDD)."""

from tests.paths import (
    EMPLOYEES,
    INSIGHTS_DISTRIBUTION,
    INSIGHTS_JOB_TITLE,
    INSIGHTS_TOP_ROLES,
)


def _seed(client) -> None:
    samples = [
        {"full_name": "A", "job_title": "Engineer", "country": "US", "salary": 80000},
        {"full_name": "B", "job_title": "Engineer", "country": "US", "salary": 120000},
        {"full_name": "C", "job_title": "Manager", "country": "US", "salary": 150000},
        {"full_name": "D", "job_title": "Engineer", "country": "UK", "salary": 70000},
        {"full_name": "E", "job_title": "Analyst", "country": "UK", "salary": 55000},
    ]
    for payload in samples:
        client.post(EMPLOYEES, json=payload)


def test_job_title_insights(client) -> None:
    _seed(client)
    response = client.get(INSIGHTS_JOB_TITLE)
    assert response.status_code == 200
    data = response.json()
    us_engineers = [
        row for row in data if row["country"] == "US" and row["job_title"] == "Engineer"
    ]
    assert len(us_engineers) == 1
    assert us_engineers[0]["avg_salary"] == 100000
    assert us_engineers[0]["employee_count"] == 2


def test_salary_distribution(client) -> None:
    _seed(client)
    response = client.get(INSIGHTS_DISTRIBUTION, params={"country": "US"})
    assert response.status_code == 200
    buckets = response.json()["buckets"]
    assert sum(b["count"] for b in buckets) == 3


def test_top_roles_by_country(client) -> None:
    _seed(client)
    response = client.get(INSIGHTS_TOP_ROLES, params={"limit": 2})
    assert response.status_code == 200
    data = response.json()
    us = next(item for item in data if item["country"] == "US")
    assert len(us["roles"]) <= 2
    assert us["roles"][0]["avg_salary"] >= us["roles"][-1]["avg_salary"]
