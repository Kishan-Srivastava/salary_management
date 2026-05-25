"""Step 3 — get employee by id (TDD)."""

from uuid import uuid4


def test_get_employee_by_id(client) -> None:
    created = client.post(
        "/employees",
        json={
            "full_name": "Jane Doe",
            "job_title": "Engineer",
            "country": "US",
            "salary": 80000,
        },
    ).json()

    response = client.get(f"/employees/{created['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created["id"]
    assert data["full_name"] == "Jane Doe"


def test_get_employee_not_found(client) -> None:
    response = client.get(f"/employees/{uuid4()}")
    assert response.status_code == 404
