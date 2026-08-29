"""Tests for product catalog routes."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_products() -> None:
    response = client.get("/products")

    assert response.status_code == 200
    body = response.json()
    ids = {item["id"] for item in body}
    assert ids == {"product_a", "product_b"}
    product_a = next(item for item in body if item["id"] == "product_a")
    assert product_a["name"] == "Product A"
    assert product_a["category"] == "Health"


def test_get_product_detail() -> None:
    response = client.get("/products/product_a")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == "product_a"
    assert body["name"] == "Product A"
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
