"""Salary insights API tests."""

from tests.test_employees_crud import _employee_payload


def _seed_employees(client) -> None:
    samples = [
        _employee_payload(country="US", job_title="Engineer", salary=80000),
        _employee_payload(country="US", job_title="Engineer", salary=120000),
        _employee_payload(country="US", job_title="Manager", salary=150000),
        _employee_payload(country="UK", job_title="Engineer", salary=70000),
        _employee_payload(country="UK", job_title="Analyst", salary=55000),
    ]
    for payload in samples:
        client.post("/employees", json=payload)


def test_country_insights(client) -> None:
    _seed_employees(client)
    response = client.get("/insights/country")
    assert response.status_code == 200
    data = response.json()
    us = next(row for row in data if row["country"] == "US")
    assert us["min_salary"] == 80000
    assert us["max_salary"] == 150000
    assert us["employee_count"] == 3
    assert 80000 <= us["avg_salary"] <= 150000


def test_job_title_insights(client) -> None:
    _seed_employees(client)
    response = client.get("/insights/job-title")
    assert response.status_code == 200
    data = response.json()
    us_engineers = [
        row
        for row in data
        if row["country"] == "US" and row["job_title"] == "Engineer"
    ]
    assert len(us_engineers) == 1
    assert us_engineers[0]["avg_salary"] == 100000
    assert us_engineers[0]["employee_count"] == 2


def test_salary_distribution(client) -> None:
    _seed_employees(client)
    response = client.get("/insights/distribution", params={"country": "US"})
    assert response.status_code == 200
    buckets = response.json()["buckets"]
    assert sum(b["count"] for b in buckets) == 3


def test_top_roles_by_country(client) -> None:
    _seed_employees(client)
    response = client.get("/insights/top-roles", params={"limit": 2})
    assert response.status_code == 200
    data = response.json()
    us = next(item for item in data if item["country"] == "US")
    assert len(us["roles"]) <= 2
    assert us["roles"][0]["avg_salary"] >= us["roles"][-1]["avg_salary"]


def test_insights_empty_database(client) -> None:
    response = client.get("/insights/country")
    assert response.status_code == 200
    assert response.json() == []
