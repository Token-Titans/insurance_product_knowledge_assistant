"""Keyword retrieval over approved markdown and PDF. No vector database."""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from app.core.errors import product_not_found
from app.services.markdown_loader import MarkdownSection, load_all_markdown, load_markdown_file
from app.services.pdf_loader import PdfPage, load_pdf_pages

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
        "what",
        "which",
        "with",
    }
)
_TOP_K = 3
_MIN_SCORE = 1.0
_PRODUCT_ID = re.compile(r"^[A-Za-z0-9_]+$")


@dataclass(frozen=True)
class RetrievedSection:
    """One ranked knowledge chunk from markdown or PDF."""

    text: str
    title: str
    file: str
    section: str
    page: int | None = None
    product_id: str = ""
    product_name: str = ""
    category: str = ""
    summary: str = ""

    @property
    def content(self) -> str:
        """Alias used by product catalog helpers."""

        return self.text

    @property
    def document(self) -> str:
        """Human-readable document title for citations."""

        return self.title

    @property
    def filename(self) -> str:
        """Source filename for citations."""

        return self.file


# Backward-compatible name used by product catalog code.
DocumentSection = RetrievedSection


@dataclass(frozen=True)
class RankedSection:
    """A retrieved section with its keyword-overlap score."""

    score: float
    section: RetrievedSection


def _safe_stem(product_id: str) -> str:
    cleaned = product_id.strip()
    if not _PRODUCT_ID.fullmatch(cleaned):
        raise product_not_found(product_id)
    return cleaned


def _approved_file(product_id: str, suffix: str) -> Path | None:
    path = (APPROVED_DIR / f"{_safe_stem(product_id)}{suffix}").resolve()
    if path.is_file() and path.parent.resolve() == APPROVED_DIR.resolve():
        return path
    return None


def product_path(product_id: str) -> Path:
    """Return the preferred approved file for a product id, or raise 404.

    Prefers `{id}.pdf` when present, otherwise `{id}.md`.
    """

    pdf_path = _approved_file(product_id, ".pdf")
    if pdf_path is not None:
        return pdf_path
    md_path = _approved_file(product_id, ".md")
    if md_path is not None:
        return md_path
    raise product_not_found(product_id)


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


def _score(question_tokens: set[str], section: RetrievedSection) -> float:
    haystack = tokenize(f"{section.title} {section.section} {section.product_name} {section.text}")
    overlap = question_tokens & haystack
    if not overlap:
        return 0.0
    heading_boost = 2.0 * len(question_tokens & tokenize(section.section))
    return float(len(overlap)) + heading_boost


def _from_markdown(chunk: MarkdownSection) -> RetrievedSection:
    return RetrievedSection(
        text=chunk.content,
        title=chunk.document,
        file=chunk.filename,
        section=chunk.section,
        page=None,
        product_id=chunk.product_id,
        product_name=chunk.product_name,
        category=chunk.category,
        summary=chunk.summary,
    )


def _from_pdf_page(page: PdfPage, product_id: str) -> RetrievedSection:
    name = product_id.replace("_", " ").title()
    return RetrievedSection(
        text=page.text,
        title=page.document,
        file=page.file,
        section=f"Page {page.page}",
        page=page.page,
        product_id=product_id,
        product_name=name,
        category="General",
        summary=page.text[:280],
    )


def _sections_for_product(product_id: str) -> list[RetrievedSection]:
    """Prefer a readable PDF; otherwise use markdown. Empty if PDF parse fails and no MD."""

    pdf_path = _approved_file(product_id, ".pdf")
    md_path = _approved_file(product_id, ".md")
    if pdf_path is not None:
        pages = load_pdf_pages(pdf_path)
        if pages:
            return [_from_pdf_page(page, _safe_stem(product_id)) for page in pages]
        if md_path is not None:
            return [_from_markdown(chunk) for chunk in load_markdown_file(md_path)]
        return []
    if md_path is not None:
        return [_from_markdown(chunk) for chunk in load_markdown_file(md_path)]
    raise product_not_found(product_id)


@lru_cache
def load_documents() -> tuple[RetrievedSection, ...]:
    """Load approved markdown, plus PDF-only products that have no markdown file."""

    if not APPROVED_DIR.is_dir():
        return ()
    documents: list[RetrievedSection] = [
        _from_markdown(chunk) for chunk in load_all_markdown(APPROVED_DIR)
    ]
    seen = {item.product_id for item in documents}
    for path in sorted(APPROVED_DIR.glob("*.pdf")):
        product_id = path.stem
        if product_id in seen:
            continue
        pages = load_pdf_pages(path)
        if not pages:
            continue
        documents.extend(_from_pdf_page(page, product_id) for page in pages)
        seen.add(product_id)
    return tuple(documents)


def search_documents(
    question: str,
    product_id: str,
    *,
    limit: int = _TOP_K,
) -> list[RankedSection]:
    """Return the top matching sections for a product question.

    Uses `{product_id}.pdf` when it parses successfully; otherwise `{product_id}.md`.
    """

    chunks = _sections_for_product(product_id)
    question_tokens = tokenize(question)
    if not question_tokens or not chunks:
        return []

    ranked = sorted(
        (
            RankedSection(score=_score(question_tokens, section), section=section)
            for section in chunks
        ),
        key=lambda item: item.score,
        reverse=True,
    )
    matched = [item for item in ranked if item.score >= _MIN_SCORE]
    return matched[:limit]
