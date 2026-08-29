"""Tests for POST /assistant/compare."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

COMPARE_QUESTION = "What are the key benefits, conditions, and exclusions?"


def test_compare_two_products() -> None:
    response = client.post(
        "/assistant/compare",
        json={
            "question": "What hospitalization benefits are paid?",
            "left_product_id": "product_a",
            "right_product_id": "product_b",
        },
    )

    assert response.status_code == 200
    body = response.json()
    left = body["left"]
    right = body["right"]
    assert left["answer"]
    assert right["answer"]
    assert "RM300" in left["answer"] or "room and board" in left["answer"].lower()
    assert "RM150" in right["answer"] or "hospital cash" in right["answer"].lower()
    assert left["source"]["file"] == "product_a.md"
    assert right["source"]["file"] == "product_b.md"
    assert 0.0 <= left["confidence"] <= 1.0
    assert 0.0 <= right["confidence"] <= 1.0


def test_compare_v1_alias() -> None:
    response = client.post(
        "/api/v1/assistant/compare",
        json={
            "question": COMPARE_QUESTION,
            "left_product_id": "dai_ichi_life_pro",
            "right_product_id": "dai_ichi_guard",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["left"]["answer"]
    assert body["right"]["answer"]
    assert body["left"]["source"]["file"]
    assert body["right"]["source"]["file"]


def test_compare_same_product_rejected() -> None:
    response = client.post(
        "/assistant/compare",
        json={
            "question": COMPARE_QUESTION,
            "left_product_id": "product_a",
            "right_product_id": "product_a",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "INVALID_REQUEST"


def test_compare_unknown_product() -> None:
    response = client.post(
        "/assistant/compare",
        json={
            "question": COMPARE_QUESTION,
            "left_product_id": "product_a",
            "right_product_id": "missing_product",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "PRODUCT_NOT_FOUND"


def test_compare_empty_question() -> None:
    response = client.post(
        "/assistant/compare",
        json={
            "question": "   ",
            "left_product_id": "product_a",
            "right_product_id": "product_b",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "INVALID_REQUEST"
