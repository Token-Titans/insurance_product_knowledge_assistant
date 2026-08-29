"""Ask orchestration: retrieve approved knowledge, then LLM or extractive answer."""

import re

from app.core.config import Settings
from app.core.errors import invalid_request, unknown_product
from app.models.assistant import AskRequest, AskResponse, SourceReference
from app.services.ai.openai_client import complete_answer
from app.services.knowledge.corpus import KNOWN_PRODUCT_IDS, KnowledgeChunk
from app.services.knowledge.retrieve import retrieve

_UNAVAILABLE_ANSWER = (
    "The approved product documents do not contain enough information to answer "
    "this question. Use a supported product brochure, benefit table, or FAQ, or "
    "identify the specific document section that would be required."
)

_CONDITION_HINTS = (
    "waiting period",
    "not covered",
    "does not pay",
    "exclusion",
    "subject to",
    "maximum",
    "up to",
    "pre-existing",
    "pre-authorisation",
    "pre-authorization",
    "must",
    "only after",
    "not payable",
    "not hospitalisation",
    "not hospitalization",
)


def _validate_product_ids(product_ids: list[str]) -> list[str]:
    cleaned: list[str] = []
    for raw in product_ids:
        value = raw.strip()
        if not value:
            continue
        if value not in KNOWN_PRODUCT_IDS:
            raise unknown_product(value)
        cleaned.append(value)
    return cleaned


def _source(chunk: KnowledgeChunk) -> SourceReference:
    return SourceReference(document=chunk.document, section=chunk.section)


def _condition_lines(chunks: list[KnowledgeChunk]) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for chunk in chunks:
        for raw_line in re.split(r"[\n.;]", chunk.text):
            line = " ".join(raw_line.split()).strip(" -*")
            lowered = line.lower()
            if len(line) < 24 or lowered in seen:
                continue
            if any(hint in lowered for hint in _CONDITION_HINTS):
                seen.add(lowered)
                found.append(line)
            if len(found) >= 4:
                return found
    return found


def _important_points(chunk: KnowledgeChunk) -> list[str]:
    points: list[str] = []
    for raw_line in chunk.text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("- "):
            point = stripped[2:].strip()
            if point:
                points.append(point)
        if len(points) >= 4:
            break
    if points:
        return points
    sentences = [
        " ".join(part.split()).strip()
        for part in re.split(r"(?<=[.!?])\s+", chunk.text)
        if len(part.strip()) > 40
    ]
    return sentences[:3]


def extractive_answer(question: str, chunks: list[KnowledgeChunk]) -> AskResponse:
    """Build a source-bounded answer without calling a model."""

    del question
    if not chunks:
        return AskResponse(
            answer=_UNAVAILABLE_ANSWER,
            important_points=[],
            conditions=[
                "Do not present this as a product fact, benefit, or exclusion."
            ],
            sources=[],
            confidence="unavailable",
        )

    top = chunks[0]
    answer = " ".join(top.text.split())
    if len(answer) > 900:
        answer = answer[:897].rsplit(" ", 1)[0] + "..."
    sources: list[SourceReference] = []
    seen: set[tuple[str, str]] = set()
    for chunk in chunks:
        key = (chunk.document, chunk.section)
        if key in seen:
            continue
        seen.add(key)
        sources.append(_source(chunk))
    return AskResponse(
        answer=answer,
        important_points=_important_points(top),
        conditions=_condition_lines(chunks),
        sources=sources,
        confidence="grounded",
    )


def ask_product_question(payload: AskRequest, settings: Settings) -> AskResponse:
    """Retrieve approved knowledge and return a grounded or unavailable answer."""

    question = payload.question.strip()
    if not question:
        raise invalid_request("question must not be empty")

    product_ids = _validate_product_ids(payload.product_ids)
    chunks = retrieve(question, product_ids)
    model_answer = complete_answer(question, chunks, settings)
    if model_answer is not None:
        return model_answer
    return extractive_answer(question, chunks)
