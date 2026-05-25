"""Step 7 — country salary insights (TDD)."""

from tests.paths import EMPLOYEES, INSIGHTS_COUNTRY


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


def test_country_insights(client) -> None:
    _seed(client)
    response = client.get(INSIGHTS_COUNTRY)
    assert response.status_code == 200
    data = response.json()
    us = next(row for row in data if row["country"] == "US")
    assert us["min_salary"] == 80000
    assert us["max_salary"] == 150000
    assert us["employee_count"] == 3
    assert 80000 <= us["avg_salary"] <= 150000


def test_country_insights_empty(client) -> None:
    response = client.get(INSIGHTS_COUNTRY)
    assert response.status_code == 200
    assert response.json() == []
