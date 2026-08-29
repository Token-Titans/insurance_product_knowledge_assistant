"""Ask orchestration: retrieve, build prompt, call OpenAI, cite retrieved sources."""

from app.core.config import Settings
from app.core.errors import invalid_request
from app.models.assistant import AssistantResponse, ProductSummary, SourceReference
from app.services.ai.openai_client import chat_json
from app.services.products import summaries_for_ids
from app.services.retrieve import DocumentSection, search_documents

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


def _sources(sections: list[DocumentSection]) -> list[SourceReference]:
    """Build citations only from retrieved sections. Never fabricate sources."""

    sources: list[SourceReference] = []
    seen: set[tuple[str, str, str]] = set()
    for section in sections:
        key = (section.title, section.filename, section.section)
        if key in seen:
            continue
        seen.add(key)
        sources.append(
            SourceReference(
                title=section.title,
                file=section.filename,
                section=section.section,
            )
        )
    return sources


def _products_from_sections(sections: list[DocumentSection]) -> list[ProductSummary]:
    return summaries_for_ids([section.product_id for section in sections])


def _context_block(sections: list[DocumentSection]) -> str:
    if not sections:
        return "Approved source excerpts: none were retrieved."
    parts = ["Approved source excerpts:"]
    for index, section in enumerate(sections, start=1):
        parts.append(
            f"[{index}] title={section.title!r} file={section.filename!r} "
            f"section={section.section!r} product_id={section.product_id!r}\n"
            f"{section.content}"
        )
    return "\n\n".join(parts)


def build_prompt(question: str, sections: list[DocumentSection]) -> list[dict[str, str]]:
    """Build the OpenAI chat messages from retrieved context."""

    user_prompt = (
        f"Question: {question}\n\n{_context_block(sections)}\n\n"
        "Return JSON with keys: answer (string), recommended_product_ids "
        "(array of product_id values copied from the excerpts). "
        "If the excerpts do not support an answer, say you don't know and "
        "use an empty recommended_product_ids array. "
        "Do not invent sources, benefits, limits, or eligibility rules."
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


async def ask_product_question(question: str, settings: Settings) -> AssistantResponse:
    """Retrieve approved sections, generate an answer, and attach real citations."""

    cleaned = question.strip()
    if not cleaned:
        raise invalid_request("question must not be empty")

    sections = search_documents(cleaned)
    generated = await chat_json(build_prompt(cleaned, sections), settings)
    sources = _sources(sections)

    if generated is None:
        return AssistantResponse(
            answer=_extractive_answer(sections),
            sources=sources,
            recommended_products=_products_from_sections(sections),
        )

    answer = str(generated.get("answer", "")).strip() or _extractive_answer(sections)
    raw_ids = generated.get("recommended_product_ids") or []
    recommended_ids = [
        str(item).strip() for item in raw_ids if str(item).strip()
    ] if isinstance(raw_ids, list) else []
    recommended = summaries_for_ids(recommended_ids) or _products_from_sections(sections)
    return AssistantResponse(
        answer=answer,
        sources=sources,
        recommended_products=recommended,
    )
