"""Approved document catalog. Product facts live only in these files."""

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

APPROVED_DIR = Path(__file__).resolve().parents[2] / "knowledge" / "approved"

KNOWN_PRODUCT_IDS = frozenset({"product-a", "product-b"})


@dataclass(frozen=True)
class ApprovedDocument:
    """Metadata for one approved knowledge file."""

    filename: str
    product_id: str
    document: str


APPROVED_DOCUMENTS: tuple[ApprovedDocument, ...] = (
    ApprovedDocument("product-a-brochure.md", "product-a", "Product A Brochure"),
    ApprovedDocument(
        "product-a-benefit-table.md", "product-a", "Product A Benefit Table"
    ),
    ApprovedDocument("product-b-brochure.md", "product-b", "Product B Brochure"),
    ApprovedDocument(
        "product-b-benefit-table.md", "product-b", "Product B Benefit Table"
    ),
    ApprovedDocument("product-faq.md", "general", "Product FAQ"),
)


@dataclass(frozen=True)
class KnowledgeChunk:
    """One retrievable section from an approved document."""

    product_id: str
    document: str
    section: str
    text: str


def _split_markdown_sections(markdown: str) -> list[tuple[str, str]]:
    """Split markdown into (section title, body) pairs on level-2 headings."""

    sections: list[tuple[str, str]] = []
    current_title = "Overview"
    current_lines: list[str] = []

    for line in markdown.splitlines():
        if line.startswith("## "):
            body = "\n".join(current_lines).strip()
            if body:
                sections.append((current_title, body))
            current_title = line[3:].strip()
            current_lines = []
            continue
        if line.startswith("# "):
            continue
        current_lines.append(line)

    body = "\n".join(current_lines).strip()
    if body:
        sections.append((current_title, body))
    return sections


@lru_cache
def load_chunks() -> tuple[KnowledgeChunk, ...]:
    """Load and chunk every approved markdown document."""

    chunks: list[KnowledgeChunk] = []
    for spec in APPROVED_DOCUMENTS:
        path = APPROVED_DIR / spec.filename
        markdown = path.read_text(encoding="utf-8")
        for section, text in _split_markdown_sections(markdown):
            chunks.append(
                KnowledgeChunk(
                    product_id=spec.product_id,
                    document=spec.document,
                    section=section,
                    text=text,
                )
            )
    return tuple(chunks)
