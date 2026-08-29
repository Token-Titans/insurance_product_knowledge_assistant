"""Tests for product catalog routes."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_products() -> None:
    response = client.get("/products")

    assert response.status_code == 200
    body = response.json()
    ids = {item["id"] for item in body}
    assert ids == {"family-care", "hospital-cash", "income-protect"}
    family = next(item for item in body if item["id"] == "family-care")
    assert family == {
        "id": "family-care",
        "name": "Family Care",
        "category": "Health",
    }


def test_get_product_detail() -> None:
    response = client.get("/products/family-care")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == "family-care"
    assert body["name"] == "Family Care"
    assert body["summary"]
    assert any("Room and board" in item for item in body["benefits"])


def test_get_unknown_product() -> None:
    response = client.get("/products/missing-id")

    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "code": "PRODUCT_NOT_FOUND",
            "message": "Unknown product 'missing-id'.",
        }
    }
