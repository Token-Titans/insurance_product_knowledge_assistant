"""Async OpenAI Chat Completions wrapper. Secrets stay in settings."""

from __future__ import annotations

import json
import logging
from typing import Any

from openai import APIError, AsyncOpenAI, OpenAIError

from app.core.config import Settings

logger = logging.getLogger(__name__)


async def chat_json(
    messages: list[dict[str, str]],
    settings: Settings,
) -> dict[str, Any] | None:
    """Call OpenAI and parse a JSON object. Return None if unconfigured or failed."""

    api_key = settings.openai_api_key.strip()
    if not api_key:
        return None

    client = AsyncOpenAI(api_key=api_key)
    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            temperature=0.2,
            response_format={"type": "json_object"},
            messages=messages,  # type: ignore[arg-type]
        )
        content = response.choices[0].message.content or ""
        parsed = json.loads(content)
        return parsed if isinstance(parsed, dict) else None
    except (APIError, OpenAIError, json.JSONDecodeError, KeyError, IndexError, TypeError):
        logger.warning("OpenAI call failed; using extractive fallback")
        return None
