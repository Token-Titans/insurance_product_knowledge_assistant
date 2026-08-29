"""Tests for POST /api/v1/assistant/ask."""

from fastapi.testclient import TestClient

from app.main import app
from app.models.assistant import AskResponse, SourceReference

client = TestClient(app)

DEMO_QUESTION = "What hospitalization benefits does Product A provide?"


def test_ask_product_a_hospital_benefits() -> None:
    response = client.post(
        "/api/v1/assistant/ask",
        json={"question": DEMO_QUESTION, "product_ids": ["product-a"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["confidence"] == "grounded"
    assert "RM300" in body["answer"] or "room and board" in body["answer"].lower()
    assert body["sources"]
    documents = {item["document"] for item in body["sources"]}
    assert "Product A Brochure" in documents or "Product A Benefit Table" in documents
    sections = {item["section"] for item in body["sources"]}
    assert "Hospital Benefits" in sections
    assert any(
        "waiting" in item.lower() or "exclusion" in item.lower() or "not" in item.lower()
        for item in body["conditions"] + body["important_points"] + [body["answer"]]
    )


def test_ask_unavailable_information() -> None:
    response = client.post(
        "/api/v1/assistant/ask",
        json={
            "question": "What is the cryptocurrency wallet protection sublimit?",
            "product_ids": ["product-a"],
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["confidence"] == "unavailable"
    assert "do not contain" in body["answer"].lower() or "unavailable" in body["answer"].lower()
    assert body["sources"] == []


def test_ask_unknown_product_id() -> None:
    response = client.post(
        "/api/v1/assistant/ask",
        json={"question": DEMO_QUESTION, "product_ids": ["product-z"]},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": {
            "code": "UNKNOWN_PRODUCT",
            "message": (
                "Unknown product_id 'product-z'. Use a supported product "
                "such as product-a or product-b."
            ),
        }
    }


def test_ask_empty_question() -> None:
    response = client.post(
        "/api/v1/assistant/ask",
        json={"question": "   "},
    )

    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "INVALID_REQUEST"


def test_ask_missing_question_field() -> None:
    response = client.post("/api/v1/assistant/ask", json={})

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "INVALID_REQUEST"


def test_ask_uses_openai_result_when_available(monkeypatch) -> None:
    grounded = AskResponse(
        answer="Product A pays room and board up to RM300 per day.",
        important_points=["Room and board up to RM300 per day."],
        conditions=["30-day waiting period except accidents."],
        sources=[
            SourceReference(
                document="Product A Brochure",
                section="Hospital Benefits",
            )
        ],
        confidence="grounded",
    )

    monkeypatch.setattr(
        "app.services.assistant.complete_answer",
        lambda question, chunks, settings: grounded,
    )

    response = client.post(
        "/api/v1/assistant/ask",
        json={"question": DEMO_QUESTION, "product_ids": ["product-a"]},
    )

    assert response.status_code == 200
    assert response.json()["answer"] == grounded.answer
    assert response.json()["confidence"] == "grounded"
