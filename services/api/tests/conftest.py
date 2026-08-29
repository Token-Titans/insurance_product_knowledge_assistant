"""Disable live OpenAI calls in tests unless a test patches the client itself."""

import pytest


@pytest.fixture(autouse=True)
def disable_live_openai(monkeypatch: pytest.MonkeyPatch, request: pytest.FixtureRequest) -> None:
    if request.node.name == "test_ask_uses_openai_result_when_available":
        return

    async def no_llm(*_args: object, **_kwargs: object) -> None:
        return None

    monkeypatch.setattr("app.services.assistant.chat_json", no_llm)
