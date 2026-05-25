"""Employee CRUD API tests."""

from uuid import UUID, uuid4


def _employee_payload(**overrides) -> dict:
    base = {
        "full_name": "Jane Doe",
        "job_title": "Software Engineer",
        "country": "US",
        "salary": 95000.00,
        "currency": "USD",
    }
    base.update(overrides)
    return base


def test_create_employee(client) -> None:
    payload = _employee_payload()
    response = client.post("/employees", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == payload["full_name"]
    assert UUID(data["id"])
    assert "created_at" in data


def test_create_employee_rejects_non_positive_salary(client) -> None:
    response = client.post("/employees", json=_employee_payload(salary=0))
    assert response.status_code == 422


def test_get_employee_by_id(client) -> None:
    created = client.post("/employees", json=_employee_payload()).json()
    response = client.get(f"/employees/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_employee_not_found(client) -> None:
    response = client.get(f"/employees/{uuid4()}")
    assert response.status_code == 404


def test_update_employee(client) -> None:
    created = client.post("/employees", json=_employee_payload()).json()
    response = client.put(
        f"/employees/{created['id']}",
        json={"salary": 120000, "job_title": "Senior Engineer"},
    )
    assert response.status_code == 200
    data = response.json()
    assert float(data["salary"]) == 120000
    assert data["job_title"] == "Senior Engineer"


def test_delete_employee(client) -> None:
    created = client.post("/employees", json=_employee_payload()).json()
    delete_resp = client.delete(f"/employees/{created['id']}")
    assert delete_resp.status_code == 204
    assert client.get(f"/employees/{created['id']}").status_code == 404


def test_list_employees_with_filters_and_pagination(client) -> None:
    client.post("/employees", json=_employee_payload(country="US", job_title="Engineer"))
    client.post("/employees", json=_employee_payload(country="UK", job_title="Analyst"))
    client.post("/employees", json=_employee_payload(country="US", job_title="Analyst"))

    all_resp = client.get("/employees")
    assert all_resp.status_code == 200
    assert all_resp.json()["total"] == 3

    us_resp = client.get("/employees", params={"country": "US"})
    assert us_resp.json()["total"] == 2

    filtered = client.get(
        "/employees",
        params={"country": "US", "job_title": "Analyst", "page": 1, "page_size": 10},
    )
    assert filtered.json()["total"] == 1
    assert filtered.json()["items"][0]["job_title"] == "Analyst"


def test_list_employees_empty(client) -> None:
    response = client.get("/employees")
    assert response.status_code == 200
    body = response.json()
    assert body["items"] == []
    assert body["total"] == 0
    assert body["pages"] == 0
