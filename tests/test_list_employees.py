"""Step 4–5 — list employees with filters (TDD)."""

from tests.paths import EMPLOYEES


def _create(
    client,
    full_name: str,
    job_title: str = "Engineer",
    country: str = "US",
) -> None:
    client.post(
        EMPLOYEES,
        json={
            "full_name": full_name,
            "job_title": job_title,
            "country": country,
            "salary": 75000,
        },
    )


def test_list_employees_empty(client) -> None:
    response = client.get(EMPLOYEES)
    assert response.status_code == 200
    body = response.json()
    assert body["items"] == []
    assert body["total"] == 0
    assert body["pages"] == 0


def test_list_employees_returns_all(client) -> None:
    _create(client, "Alice")
    _create(client, "Bob", country="UK")

    response = client.get(EMPLOYEES)
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    names = {item["full_name"] for item in body["items"]}
    assert names == {"Alice", "Bob"}


def test_filter_job_title_partial_match(client) -> None:
    _create(client, "Ann", job_title="Financial Analyst")
    _create(client, "Ben", job_title="Software Engineer")
    _create(client, "Cal", job_title="Senior Finance Manager")

    response = client.get(EMPLOYEES, params={"job_title": "finance"})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    titles = {item["job_title"] for item in body["items"]}
    assert titles == {"Financial Analyst", "Senior Finance Manager"}


def test_filter_job_title_case_insensitive(client) -> None:
    _create(client, "Dana", job_title="Financial Analyst")

    response = client.get(EMPLOYEES, params={"job_title": "FINANCE"})
    assert response.status_code == 200
    assert response.json()["total"] == 1


def test_filter_by_country(client) -> None:
    _create(client, "Eve", job_title="Engineer", country="US")
    _create(client, "Finn", job_title="Engineer", country="UK")

    response = client.get(EMPLOYEES, params={"country": "UK"})
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["country"] == "UK"


def test_filter_by_name_partial_match(client) -> None:
    _create(client, "John Smith", job_title="Engineer")
    _create(client, "Jane Williams", job_title="Analyst")
    _create(client, "Johnny Bravo", job_title="Designer")

    response = client.get(EMPLOYEES, params={"full_name": "john"})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    names = {item["full_name"] for item in body["items"]}
    assert names == {"John Smith", "Johnny Bravo"}


def test_filter_name_excludes_stem_false_positives(client) -> None:
    _create(client, "Kishan Patel")
    _create(client, "Kristin Jones")
    _create(client, "Ankit Singh")

    response = client.get(EMPLOYEES, params={"full_name": "kish"})
    assert response.status_code == 200
    names = {item["full_name"] for item in response.json()["items"]}
    assert names == {"Kishan Patel"}


def test_filter_by_name_and_job_title(client) -> None:
    _create(client, "Alice Finance", job_title="Financial Analyst")
    _create(client, "Bob Finance", job_title="Software Engineer")

    response = client.get(
        EMPLOYEES,
        params={"full_name": "alice", "job_title": "finance"},
    )
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["full_name"] == "Alice Finance"


def test_filter_by_emp_id_partial(client) -> None:
    r1 = client.post(
        EMPLOYEES,
        json={
            "full_name": "One",
            "job_title": "Engineer",
            "country": "US",
            "salary": 75000,
        },
    )
    r2 = client.post(
        EMPLOYEES,
        json={
            "full_name": "Two",
            "job_title": "Engineer",
            "country": "US",
            "salary": 75000,
        },
    )
    emp1 = r1.json()["emp_id"]
    emp2 = r2.json()["emp_id"]

    response = client.get(EMPLOYEES, params={"emp_id": str(emp1)[:1]})
    assert response.status_code == 200
    ids = {item["emp_id"] for item in response.json()["items"]}
    assert emp1 in ids or emp2 in ids


def test_get_by_emp_id(client) -> None:
    created = client.post(
        EMPLOYEES,
        json={
            "full_name": "Lookup",
            "job_title": "Engineer",
            "country": "US",
            "salary": 75000,
        },
    ).json()
    response = client.get(f"{EMPLOYEES}/by-emp-id/{created['emp_id']}")
    assert response.status_code == 200
    assert response.json()["full_name"] == "Lookup"


def test_list_pagination(client) -> None:
    for i in range(5):
        _create(client, f"Person{i}")

    response = client.get(EMPLOYEES, params={"page": 1, "page_size": 2})
    body = response.json()
    assert body["total"] == 5
    assert len(body["items"]) == 2
    assert body["pages"] == 3
