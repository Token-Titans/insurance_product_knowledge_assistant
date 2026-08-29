"""Keyword retrieval over the approved corpus. No vector database."""

import re

from app.services.knowledge.corpus import KnowledgeChunk, load_chunks

_STOPWORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "are",
        "does",
        "for",
        "from",
        "how",
        "in",
        "is",
        "of",
        "on",
        "or",
        "the",
        "to",
        "what",
        "when",
        "which",
        "with",
    }
)

_MIN_SCORE = 1.5
_MAX_CHUNKS = 4


def _expand_token(token: str) -> set[str]:
    variants = {token}
    if token.endswith("ization") and len(token) > 10:
        variants.add(token[: -len("ization")])
    if token.endswith("isation") and len(token) > 10:
        variants.add(token[: -len("isation")])
    if token.endswith("ing") and len(token) > 5:
        variants.add(token[:-3])
    if token.endswith("ed") and len(token) > 4:
        variants.add(token[:-2])
    if token.endswith("s") and len(token) > 3:
        variants.add(token[:-1])
    return variants


def tokenize(text: str) -> set[str]:
    """Return expanded content tokens for overlap scoring."""

    tokens: set[str] = set()
    for raw in re.findall(r"[a-z0-9]+", text.lower()):
        if raw in _STOPWORDS or len(raw) < 2:
            continue
        tokens.update(_expand_token(raw))
    return tokens


def _score(question_tokens: set[str], chunk: KnowledgeChunk) -> float:
    haystack = tokenize(f"{chunk.document} {chunk.section} {chunk.text}")
    overlap = question_tokens & haystack
    if not overlap:
        return 0.0
    section_boost = 2.0 * len(question_tokens & tokenize(chunk.section))
    return float(len(overlap)) + section_boost


def retrieve(
    question: str,
    product_ids: list[str] | None = None,
    *,
    limit: int = _MAX_CHUNKS,
) -> list[KnowledgeChunk]:
    """Return the highest-scoring approved sections for a question."""

    chunks = load_chunks()
    requested = [item.strip() for item in (product_ids or []) if item.strip()]
    if requested:
        allowed = set(requested)
        allowed.add("general")
        chunks = tuple(
            chunk for chunk in chunks if chunk.product_id in allowed
        )

    question_tokens = tokenize(question)
    if not question_tokens:
        return []

    ranked = sorted(
        ((_score(question_tokens, chunk), chunk) for chunk in chunks),
        key=lambda item: item[0],
        reverse=True,
    )
    selected = [chunk for score, chunk in ranked if score >= _MIN_SCORE]
    return selected[:limit]
