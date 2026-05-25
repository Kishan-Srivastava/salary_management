"""Step 6 — update and delete employee (TDD)."""

from uuid import uuid4


def _create(client) -> dict:
    response = client.post(
        "/employees",
        json={
            "full_name": "Jane Doe",
            "job_title": "Engineer",
            "country": "US",
            "salary": 80000,
        },
    )
    return response.json()


def test_update_full_name(client) -> None:
    created = _create(client)
    response = client.put(
        f"/employees/{created['id']}",
        json={"full_name": "Janet Smith"},
    )
    assert response.status_code == 200
    assert response.json()["full_name"] == "Janet Smith"


def test_update_employee(client) -> None:
    created = _create(client)
    response = client.put(
        f"/employees/{created['id']}",
        json={"salary": 95000, "job_title": "Senior Engineer"},
    )
    assert response.status_code == 200
    data = response.json()
    assert float(data["salary"]) == 95000
    assert data["job_title"] == "Senior Engineer"
    assert data["full_name"] == "Jane Doe"


def test_update_employee_not_found(client) -> None:
    response = client.put(
        f"/employees/{uuid4()}",
        json={"salary": 100000},
    )
    assert response.status_code == 404


def test_update_rejects_zero_salary(client) -> None:
    created = _create(client)
    response = client.put(
        f"/employees/{created['id']}",
        json={"salary": 0},
    )
    assert response.status_code == 422


def test_delete_employee(client) -> None:
    created = _create(client)
    delete_resp = client.delete(f"/employees/{created['id']}")
    assert delete_resp.status_code == 204
    assert client.get(f"/employees/{created['id']}").status_code == 404


def test_delete_employee_not_found(client) -> None:
    response = client.delete(f"/employees/{uuid4()}")
    assert response.status_code == 404


def test_update_by_emp_id(client) -> None:
    created = _create(client)
    response = client.put(
        f"/employees/by-emp-id/{created['emp_id']}",
        json={"full_name": "Updated Via Emp Id"},
    )
    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated Via Emp Id"


def test_delete_by_emp_id(client) -> None:
    created = _create(client)
    delete_resp = client.delete(f"/employees/by-emp-id/{created['emp_id']}")
    assert delete_resp.status_code == 204
    assert client.get(f"/employees/by-emp-id/{created['emp_id']}").status_code == 404
