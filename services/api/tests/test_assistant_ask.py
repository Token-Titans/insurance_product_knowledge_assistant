"""Tests for POST /assistant/ask."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

SUITABILITY_QUESTION = "I am 30 years old. Which insurance is suitable?"


def test_ask_suitability_returns_sources_and_products() -> None:
    response = client.post(
        "/assistant/ask",
        json={"question": SUITABILITY_QUESTION},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["answer"]
    assert body["sources"]
    files = {item["file"] for item in body["sources"]}
    assert files <= {"family_care.md", "hospital_cash.md", "income_protect.md"}
    for source in body["sources"]:
        assert source["title"]
        assert source["section"]
    ids = {item["id"] for item in body["recommended_products"]}
    assert "family-care" in ids or "hospital-cash" in ids or "income-protect" in ids


def test_ask_v1_alias() -> None:
    response = client.post(
        "/api/v1/assistant/ask",
        json={"question": "What hospitalisation benefits does Family Care provide?"},
    )

    assert response.status_code == 200
    body = response.json()
    assert "sources" in body
    assert "recommended_products" in body
    assert "important_points" not in body


def test_ask_unavailable_information() -> None:
    response = client.post(
        "/assistant/ask",
        json={"question": "What is the cryptocurrency wallet protection sublimit?"},
    )

    assert response.status_code == 200
    body = response.json()
    assert "don't know" in body["answer"].lower() or "do not contain" in body["answer"].lower()


def test_ask_empty_question() -> None:
    response = client.post("/assistant/ask", json={"question": "   "})

    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "INVALID_REQUEST"


def test_ask_missing_question_field() -> None:
    response = client.post("/assistant/ask", json={})

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "INVALID_REQUEST"


def test_ask_uses_openai_result_when_available(monkeypatch) -> None:
    async def fake_chat_json(messages, settings):
        del messages, settings
        return {
            "answer": "Recommended product is Family Care for a 30-year-old working adult.",
            "recommended_product_ids": ["family-care"],
        }

    monkeypatch.setattr("app.services.assistant.chat_json", fake_chat_json)

    response = client.post(
        "/assistant/ask",
        json={"question": SUITABILITY_QUESTION},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["answer"].startswith("Recommended product is Family Care")
    assert body["recommended_products"][0]["id"] == "family-care"
    assert body["sources"]
