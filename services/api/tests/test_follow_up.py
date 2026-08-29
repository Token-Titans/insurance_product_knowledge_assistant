"""Tests for POST /assistant/follow-up."""

from datetime import date, timedelta

from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app

client = TestClient(app)

FUTURE = (date.today() + timedelta(days=7)).isoformat()

VALID_BODY = {
    "customer_name": "Aung Aung",
    "product_id": "product_a",
    "follow_up_date": FUTURE,
    "note": "Call back about hospitalization benefits.",
}


def test_follow_up_unconfigured(monkeypatch) -> None:
    monkeypatch.setenv("N8N_WEBHOOK_URL", "")
    get_settings.cache_clear()
    response = client.post("/assistant/follow-up", json=VALID_BODY)

    assert response.status_code == 503
    assert response.json()["detail"]["code"] == "AUTOMATION_UNAVAILABLE"


def test_follow_up_unknown_product(monkeypatch) -> None:
    get_settings.cache_clear()
    monkeypatch.setenv("N8N_WEBHOOK_URL", "https://example.test/webhook")
    get_settings.cache_clear()

    response = client.post(
        "/assistant/follow-up",
        json={**VALID_BODY, "product_id": "missing_product"},
    )

    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "PRODUCT_NOT_FOUND"
    get_settings.cache_clear()


def test_follow_up_rejects_past_date(monkeypatch) -> None:
    get_settings.cache_clear()
    monkeypatch.setenv("N8N_WEBHOOK_URL", "https://example.test/webhook")
    get_settings.cache_clear()

    response = client.post(
        "/assistant/follow-up",
        json={**VALID_BODY, "follow_up_date": "2020-01-01"},
    )

    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "INVALID_REQUEST"
    get_settings.cache_clear()


def test_follow_up_posts_n8n_payload(monkeypatch) -> None:
    captured: dict[str, object] = {}

    async def fake_post(url: str, payload: dict[str, object]) -> None:
        captured["url"] = url
        captured["payload"] = payload

    monkeypatch.setenv("N8N_WEBHOOK_URL", "https://example.test/webhook")
    get_settings.cache_clear()
    monkeypatch.setattr("app.services.follow_up.post_webhook", fake_post)

    response = client.post("/assistant/follow-up", json=VALID_BODY)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "scheduled"
    assert body["customer_name"] == "Aung Aung"
    assert body["product"] == "Product A"
    assert body["follow_up_date"] == FUTURE
    assert captured["url"] == "https://example.test/webhook"
    assert captured["payload"] == {
        "customer_name": "Aung Aung",
        "product": "Product A",
        "product_id": "product_a",
        "follow_up_date": FUTURE,
        "note": "Call back about hospitalization benefits.",
    }
    get_settings.cache_clear()
