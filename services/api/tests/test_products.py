"""Tests for product catalog routes."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_products() -> None:
    response = client.get("/products")

    assert response.status_code == 200
    body = response.json()
    ids = {item["id"] for item in body}
    assert ids == {
        "product_a",
        "product_b",
        "dai_ichi_life_pro",
        "dai_ichi_guard",
        "dai_ichi_ci_plus",
        "dai_ichi_active_care",
        "htar_wa_ra_edu_goal",
    }
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


def test_list_suggested_questions_for_product_a() -> None:
    response = client.get("/products/product_a/suggested-questions")

    assert response.status_code == 200
    body = response.json()
    ids = [item["id"] for item in body]
    assert ids == ["hospitalization", "eligibility", "conditions", "exclusions"]
    hospitalization = body[0]
    assert hospitalization["title"] == "Hospitalization"
    assert hospitalization["question"] == (
        "What hospitalization benefits does Product A provide?"
    )


def test_list_suggested_questions_for_catalog_product() -> None:
    response = client.get("/products/dai_ichi_life_pro/suggested-questions")

    assert response.status_code == 200
    body = response.json()
    assert 1 <= len(body) <= 5
    ids = [item["id"] for item in body]
    assert "benefits" in ids
    assert "eligibility" in ids
    assert "exclusions" in ids
    assert all("Dai-ichi Life Pro" in item["question"] for item in body)


def test_list_suggested_questions_unknown_product() -> None:
    response = client.get("/products/missing-id/suggested-questions")

    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "code": "PRODUCT_NOT_FOUND",
            "message": "Unknown product 'missing-id'.",
        }
    }


def test_list_products_v1_alias() -> None:
    response = client.get("/api/v1/products")

    assert response.status_code == 200
    ids = {item["id"] for item in response.json()}
    assert "dai_ichi_life_pro" in ids
    assert "product_a" in ids
