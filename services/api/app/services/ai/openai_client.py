"""OpenAI Chat Completions client. Key stays server-side and may be unset."""

import json
import logging
from typing import Any

import httpx

from app.core.config import Settings
from app.models.assistant import AskResponse, SourceReference
from app.services.ai.prompts import SYSTEM_PROMPT, build_user_prompt
from app.services.knowledge.corpus import KnowledgeChunk

logger = logging.getLogger(__name__)

_OPENAI_URL = "https://api.openai.com/v1/chat/completions"
_TIMEOUT_SECONDS = 20.0


def _allowed_sources(chunks: list[KnowledgeChunk]) -> set[tuple[str, str]]:
    return {(chunk.document, chunk.section) for chunk in chunks}


def _coerce_response(
    payload: dict[str, Any], chunks: list[KnowledgeChunk]
) -> AskResponse | None:
    """Validate model JSON against the API schema and approved citations."""

    try:
        confidence = payload.get("confidence")
        if confidence not in {"grounded", "unavailable"}:
            return None
        sources_raw = payload.get("sources") or []
        if not isinstance(sources_raw, list):
            return None
        allowed = _allowed_sources(chunks)
        sources: list[SourceReference] = []
        for item in sources_raw:
            if not isinstance(item, dict):
                continue
            document = str(item.get("document", "")).strip()
            section = str(item.get("section", "")).strip()
            if (document, section) in allowed:
                sources.append(SourceReference(document=document, section=section))
        if confidence == "grounded" and not sources and chunks:
            top = chunks[0]
            sources = [SourceReference(document=top.document, section=top.section)]
        answer = str(payload.get("answer", "")).strip()
        if not answer:
            return None
        important = payload.get("important_points") or []
        conditions = payload.get("conditions") or []
        if not isinstance(important, list) or not isinstance(conditions, list):
            return None
        return AskResponse(
            answer=answer,
            important_points=[str(item).strip() for item in important if str(item).strip()],
            conditions=[str(item).strip() for item in conditions if str(item).strip()],
            sources=sources,
            confidence=confidence,
        )
    except (TypeError, ValueError):
        return None


def complete_answer(
    question: str,
    chunks: list[KnowledgeChunk],
    settings: Settings,
) -> AskResponse | None:
    """Call OpenAI when a key is configured. Return None to use extractive fallback."""

    api_key = settings.openai_api_key.strip()
    if not api_key:
        return None

    body = {
        "model": settings.openai_model,
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(question, chunks)},
        ],
    }
    try:
        response = httpx.post(
            _OPENAI_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=body,
            timeout=_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            return None
        return _coerce_response(parsed, chunks)
    except (httpx.HTTPError, KeyError, IndexError, json.JSONDecodeError, TypeError):
        logger.warning("OpenAI grounded-answer call failed; using extractive fallback")
        return None
