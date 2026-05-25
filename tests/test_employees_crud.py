"""Employee CRUD API tests."""

from uuid import UUID


def test_create_employee(client) -> None:
    payload = {
        "full_name": "Jane Doe",
        "job_title": "Software Engineer",
        "country": "US",
        "salary": 95000.00,
        "currency": "USD",
    }
    response = client.post("/employees", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == payload["full_name"]
    assert data["job_title"] == payload["job_title"]
    assert data["country"] == payload["country"]
    assert float(data["salary"]) == payload["salary"]
    assert data["currency"] == "USD"
    assert UUID(data["id"])
    assert "created_at" in data
    assert "updated_at" in data
