"""PDF retrieval prefers `{id}.pdf` and falls back to markdown if parse fails."""

from pathlib import Path

from app.services.pdf_loader import PdfPage
from app.services.retrieve import load_documents, search_documents


def test_search_prefers_pdf_when_parse_succeeds(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "product_a.pdf").write_bytes(b"%PDF-1.4 placeholder")
    (tmp_path / "product_a.md").write_text(
        "# Product A\n\n## Hospitalization Benefits\nMarkdown hospitalization RM1 only.\n",
        encoding="utf-8",
    )
    monkeypatch.setattr("app.services.retrieve.APPROVED_DIR", tmp_path)
    monkeypatch.setattr(
        "app.services.retrieve.load_pdf_pages",
        lambda _path: [
            PdfPage(
                text="PDF hospitalization benefit RM999 per day for inpatient confinement.",
                page=2,
                document="Product A Brochure",
                file="product_a.pdf",
            )
        ],
    )
    load_documents.cache_clear()

    ranked = search_documents("What is the hospitalization benefit?", "product_a")

    assert ranked
    top = ranked[0].section
    assert top.file == "product_a.pdf"
    assert top.page == 2
    assert top.section == "Page 2"
    assert "RM999" in top.text


def test_search_falls_back_to_markdown_when_pdf_unreadable(
    tmp_path: Path, monkeypatch
) -> None:
    (tmp_path / "product_a.pdf").write_bytes(b"not-a-pdf")
    (tmp_path / "product_a.md").write_text(
        "# Product A\n\n## Hospitalization Benefits\nRoom and board up to RM300 per day.\n",
        encoding="utf-8",
    )
    monkeypatch.setattr("app.services.retrieve.APPROVED_DIR", tmp_path)
    monkeypatch.setattr("app.services.retrieve.load_pdf_pages", lambda _path: [])
    load_documents.cache_clear()

    ranked = search_documents("What is the hospitalization benefit?", "product_a")

    assert ranked
    top = ranked[0].section
    assert top.file == "product_a.md"
    assert top.page is None
    assert "RM300" in top.text


def test_search_accepts_hyphenated_dai_ichi_id() -> None:
    load_documents.cache_clear()
    ranked = search_documents("What is the living benefit?", "dai-ichi-life-pro")

    assert ranked
    assert ranked[0].section.product_id == "dai-ichi-life-pro"


def test_search_maps_burmese_benefit_question() -> None:
    load_documents.cache_clear()
    ranked = search_documents("အကျိုးခံစားခွင့်က ဘာလဲ။", "product_a")

    assert ranked
    assert ranked[0].score >= 1.0
