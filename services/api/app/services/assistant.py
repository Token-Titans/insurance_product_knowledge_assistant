"""Ask orchestration: retrieve one product file, then OpenAI or extractive fallback."""

import re

from app.core.config import Settings
from app.core.errors import invalid_request
from app.models.assistant import AssistantResponse, SourceReference
from app.services.ai.openai_client import chat_json
from app.services.retrieve import DocumentSection, RankedSection, search_documents

SYSTEM_PROMPT = (
    "You are an insurance product knowledge assistant. "
    "Only answer using provided context. "
    "If information is unavailable, say you don't know. "
    "Never invent insurance benefits."
)

_UNAVAILABLE_ANSWER = (
    "I don't know. The approved product documents do not contain enough "
    "information to answer this question."
)

_CONDITION_HINTS = (
    "waiting period",
    "pre-authorisation",
    "pre-authorization",
    "subject to",
    "must",
    "only after",
    "not payable",
    "annual aggregate",
)
_EXCLUSION_HINTS = (
    "does not pay",
    "not covered",
    "exclusion",
    "not pay for",
)


def _empty_source() -> SourceReference:
    return SourceReference(document="", file="", section="")


def _source_from(section: DocumentSection) -> SourceReference:
    """Copy citation fields from a retrieved section only."""

    return SourceReference(
        document=section.document,
        file=section.filename,
        section=section.section,
    )


def _confidence(ranked: list[RankedSection]) -> float:
    """Map the top keyword score onto a 0.0–1.0 range."""

    if not ranked:
        return 0.0
    return round(min(1.0, ranked[0].score / 10.0), 2)


def _bullet_or_sentence_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw in re.split(r"[\n;]", text):
        item = " ".join(raw.split()).strip(" -*")
        if len(item) >= 24:
            lines.append(item)
    return lines


def _extract_labeled(sections: list[DocumentSection], heading: str, hints: tuple[str, ...]) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for section in sections:
        relevant = heading in section.section.lower()
        for line in _bullet_or_sentence_lines(section.content):
            lowered = line.lower()
            if lowered in seen:
                continue
            if relevant or any(hint in lowered for hint in hints):
                seen.add(lowered)
                found.append(line)
            if len(found) >= 5:
                return found
    return found


def _context_block(sections: list[DocumentSection]) -> str:
    if not sections:
        return "Approved source excerpts: none were retrieved."
    parts = ["Approved source excerpts:"]
    for index, section in enumerate(sections, start=1):
        parts.append(
            f"[{index}] document={section.document!r} file={section.filename!r} "
            f"section={section.section!r}\n{section.content}"
        )
    return "\n\n".join(parts)


def build_prompt(question: str, sections: list[DocumentSection]) -> list[dict[str, str]]:
    """Build OpenAI chat messages from the top retrieved sections."""

    user_prompt = (
        f"Question: {question}\n\n{_context_block(sections)}\n\n"
        "Return JSON with keys: answer (string), important_conditions (array of strings), "
        "exclusions (array of strings). "
        "Copy conditions and exclusions only from the excerpts. "
        "If the excerpts do not support an answer, say you don't know and use empty arrays. "
        "Do not invent benefits, limits, waiting periods, or exclusions."
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


def _extractive_answer(sections: list[DocumentSection]) -> str:
    if not sections:
        return _UNAVAILABLE_ANSWER
    text = " ".join(sections[0].content.split())
    if len(text) > 900:
        text = text[:897].rsplit(" ", 1)[0] + "..."
    return text


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


async def ask_product_question(
    product_id: str,
    question: str,
    settings: Settings,
) -> AssistantResponse:
    """Retrieve one product file, generate an answer, and attach a real citation."""

    cleaned_product = product_id.strip()
    cleaned_question = question.strip()
    if not cleaned_product:
        raise invalid_request("product_id must not be empty")
    if not cleaned_question:
        raise invalid_request("question must not be empty")

    ranked = search_documents(cleaned_question, cleaned_product)
    sections = [item.section for item in ranked]
    generated = await chat_json(build_prompt(cleaned_question, sections), settings)

    source = _source_from(sections[0]) if sections else _empty_source()
    fallback_conditions = _extract_labeled(sections, "condition", _CONDITION_HINTS)
    fallback_exclusions = _extract_labeled(sections, "exclusion", _EXCLUSION_HINTS)

    if generated is None:
        return AssistantResponse(
            answer=_extractive_answer(sections),
            important_conditions=fallback_conditions,
            exclusions=fallback_exclusions,
            source=source,
            confidence=_confidence(ranked),
        )

    answer = str(generated.get("answer", "")).strip() or _extractive_answer(sections)
    return AssistantResponse(
        answer=answer,
        important_conditions=_string_list(generated.get("important_conditions"))
        or fallback_conditions,
        exclusions=_string_list(generated.get("exclusions")) or fallback_exclusions,
        source=source,
        confidence=_confidence(ranked),
    )
