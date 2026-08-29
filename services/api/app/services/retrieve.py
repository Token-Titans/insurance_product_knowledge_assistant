"""Keyword retrieval over approved markdown. No vector database."""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

APPROVED_DIR = Path(__file__).resolve().parents[1] / "knowledge" / "approved"

_STOPWORDS = frozenset(
    {
        "a",
        "am",
        "an",
        "and",
        "are",
        "for",
        "from",
        "i",
        "in",
        "is",
        "of",
        "on",
        "or",
        "the",
        "to",
        "which",
        "with",
    }
)
_TOP_K = 3
_MIN_SCORE = 1.0
_HEADING = re.compile(r"^(#{1,2})\s+(.+?)\s*$")


@dataclass(frozen=True)
class DocumentSection:
    """One heading-bounded section from an approved markdown file."""

    product_id: str
    product_name: str
    category: str
    summary: str
    title: str
    filename: str
    section: str
    content: str


def _slug_from_filename(filename: str) -> str:
    stem = Path(filename).stem
    return stem.replace("_", "-").replace(" ", "-").lower()


def _parse_frontmatter(raw: str) -> tuple[dict[str, str], str]:
    """Parse optional `---` YAML-like metadata. Unknown keys are ignored."""

    text = raw.lstrip("\ufeff")
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    block = text[3:end].strip()
    body = text[end + 4 :].lstrip("\n")
    meta: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip().lower()] = value.strip().strip("\"'")
    return meta, body


def _split_sections(markdown: str) -> list[tuple[str, str]]:
    """Split markdown on `#` and `##` headings."""

    sections: list[tuple[str, str]] = []
    current_title = "Overview"
    current_lines: list[str] = []
    for line in markdown.splitlines():
        match = _HEADING.match(line)
        if match:
            body = "\n".join(current_lines).strip()
            if body:
                sections.append((current_title, body))
            current_title = match.group(2).strip()
            current_lines = []
            continue
        current_lines.append(line)
    body = "\n".join(current_lines).strip()
    if body:
        sections.append((current_title, body))
    return sections


def _expand_token(token: str) -> set[str]:
    variants = {token}
    if token.endswith("ization") and len(token) > 10:
        variants.add(token[: -len("ization")])
    if token.endswith("s") and len(token) > 3:
        variants.add(token[:-1])
    return variants


def tokenize(text: str) -> set[str]:
    """Return content tokens used for overlap scoring."""

    tokens: set[str] = set()
    for raw in re.findall(r"[a-z0-9]+", text.lower()):
        if raw in _STOPWORDS or len(raw) < 2:
            continue
        tokens.update(_expand_token(raw))
    return tokens


def _score(question_tokens: set[str], section: DocumentSection) -> float:
    haystack = tokenize(
        f"{section.title} {section.section} {section.product_name} {section.content}"
    )
    overlap = question_tokens & haystack
    if not overlap:
        return 0.0
    heading_boost = 2.0 * len(question_tokens & tokenize(section.section))
    return float(len(overlap)) + heading_boost


@lru_cache
def load_documents() -> tuple[DocumentSection, ...]:
    """Load every markdown file in the approved corpus and split by heading."""

    if not APPROVED_DIR.is_dir():
        return ()

    documents: list[DocumentSection] = []
    for path in sorted(APPROVED_DIR.glob("*.md")):
        meta, body = _parse_frontmatter(path.read_text(encoding="utf-8"))
        product_id = meta.get("id") or _slug_from_filename(path.name)
        first_heading = next(
            (title for title, _content in _split_sections(body) if title != "Overview"),
            path.stem.replace("_", " ").title(),
        )
        product_name = meta.get("name") or first_heading
        title = meta.get("title") or f"{product_name} Brochure"
        category = meta.get("category") or "General"
        summary = meta.get("summary") or ""
        for section_name, content in _split_sections(body):
            documents.append(
                DocumentSection(
                    product_id=product_id,
                    product_name=product_name,
                    category=category,
                    summary=summary,
                    title=title,
                    filename=path.name,
                    section=section_name,
                    content=content,
                )
            )
    return tuple(documents)


def search_documents(question: str, *, limit: int = _TOP_K) -> list[DocumentSection]:
    """Return the top matching approved sections for a question."""

    question_tokens = tokenize(question)
    if not question_tokens:
        return []

    ranked = sorted(
        ((_score(question_tokens, section), section) for section in load_documents()),
        key=lambda item: item[0],
        reverse=True,
    )
    matched = [section for score, section in ranked if score >= _MIN_SCORE]
    return matched[:limit]
