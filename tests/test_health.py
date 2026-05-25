"""Health endpoint tests."""

from app.core.version import API_V1_PREFIX, API_VERSION, APP_VERSION


def test_health_liveness(client) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_v1_returns_version(client) -> None:
    response = client.get(f"{API_V1_PREFIX}/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["app_version"] == APP_VERSION
    assert body["api_version"] == API_VERSION
