"""Load approved PDF files page by page. Failures return an empty list."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PdfPage:
    """One extracted PDF page from an approved product file."""

    text: str
    page: int
    document: str
    file: str


def load_pdf_pages(path: Path) -> list[PdfPage]:
    """Read every page of a PDF. Return [] if the file cannot be parsed."""

    try:
        import pdfplumber
    except ImportError:
        logger.warning("pdfplumber is not installed; skipping PDF %s", path.name)
        return []

    document = f"{path.stem.replace('_', ' ').title()} Brochure"
    pages: list[PdfPage] = []
    try:
        with pdfplumber.open(path) as pdf:
            for index, page in enumerate(pdf.pages, start=1):
                extracted = page.extract_text() or ""
                text = " ".join(extracted.split()).strip()
                if not text:
                    continue
                pages.append(
                    PdfPage(
                        text=text,
                        page=index,
                        document=document,
                        file=path.name,
                    )
                )
    except Exception:
        logger.warning("Failed to parse PDF %s; falling back if markdown exists", path.name)
        return []
    return pages
