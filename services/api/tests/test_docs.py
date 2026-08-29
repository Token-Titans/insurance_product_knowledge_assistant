"""Swagger availability."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_swagger_docs_available() -> None:
    response = client.get("/docs")

    assert response.status_code == 200
    assert "swagger" in response.text.lower() or "openapi" in response.text.lower()


def test_openapi_schema_includes_frozen_paths() -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/health" in paths
    assert "/products" in paths
    assert "/products/{id}" in paths
    assert "/products/{id}/suggested-questions" in paths
    assert "/assistant/ask" in paths
    assert "/assistant/compare" in paths
    assert "/assistant/follow-up" in paths
