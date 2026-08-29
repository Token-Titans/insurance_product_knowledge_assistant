"""Tests for POST /assistant/ask."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

HOSPITAL_QUESTION = "What is the hospitalization benefit?"


def test_ask_product_a_hospitalization() -> None:
    response = client.post(
        "/assistant/ask",
        json={"product_id": "product_a", "question": HOSPITAL_QUESTION},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["answer"]
    assert "RM300" in body["answer"] or "room and board" in body["answer"].lower()
    assert body["source"]["file"] == "product_a.md"
    assert body["source"]["document"]
    assert body["source"]["section"]
    assert "page" not in body["source"]
    assert isinstance(body["important_conditions"], list)
    assert isinstance(body["exclusions"], list)
    assert 0.0 <= body["confidence"] <= 1.0
    assert body["confidence"] > 0.0


def test_ask_unknown_product() -> None:
    response = client.post(
        "/assistant/ask",
        json={"product_id": "missing_product", "question": HOSPITAL_QUESTION},
    )

    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "PRODUCT_NOT_FOUND"


def test_ask_unavailable_information() -> None:
    response = client.post(
        "/assistant/ask",
        json={
            "product_id": "product_a",
            "question": "What is the cryptocurrency wallet protection sublimit?",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["confidence"] == 0.0
    assert body["source"] == {"document": "", "file": "", "section": ""}


def test_ask_empty_question() -> None:
    response = client.post(
        "/assistant/ask",
        json={"product_id": "product_a", "question": "   "},
    )

    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "INVALID_REQUEST"


def test_ask_missing_fields() -> None:
    response = client.post("/assistant/ask", json={"question": HOSPITAL_QUESTION})

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "INVALID_REQUEST"


def test_ask_uses_openai_result_when_available(monkeypatch) -> None:
    async def fake_chat_json(messages, settings):
        del messages, settings
        return {
            "answer": "Product A pays room and board up to RM300 per day.",
            "important_conditions": ["30-day waiting period except accidents."],
            "exclusions": ["Cosmetic procedures are not covered."],
        }

    monkeypatch.setattr("app.services.assistant.chat_json", fake_chat_json)

    response = client.post(
        "/assistant/ask",
        json={"product_id": "product_a", "question": HOSPITAL_QUESTION},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["answer"].startswith("Product A pays room and board")
    assert body["important_conditions"] == ["30-day waiting period except accidents."]
    assert body["exclusions"] == ["Cosmetic procedures are not covered."]
    assert body["source"]["file"] == "product_a.md"
