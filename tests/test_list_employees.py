"""Step 4 — list employees (TDD)."""


def _create(client, name: str, country: str = "US") -> None:
    client.post(
        "/employees",
        json={
            "full_name": name,
            "job_title": "Engineer",
            "country": country,
            "salary": 75000,
        },
    )


def test_list_employees_empty(client) -> None:
    response = client.get("/employees")
    assert response.status_code == 200
    assert response.json() == []


def test_list_employees_returns_all(client) -> None:
    _create(client, "Alice")
    _create(client, "Bob", country="UK")

    response = client.get("/employees")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    names = {item["full_name"] for item in data}
    assert names == {"Alice", "Bob"}
