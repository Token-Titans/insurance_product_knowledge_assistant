"""Load approved markdown files and split them on headings."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

_HEADING = re.compile(r"^(#{1,2})\s+(.+?)\s*$")


@dataclass(frozen=True)
class MarkdownSection:
    """One heading-bounded section from an approved markdown file."""

    product_id: str
    product_name: str
    category: str
    summary: str
    document: str
    filename: str
    section: str
    content: str


def parse_frontmatter(raw: str) -> tuple[dict[str, str], str]:
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


def split_sections(markdown: str) -> list[tuple[str, str]]:
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


def load_markdown_file(path: Path) -> list[MarkdownSection]:
    """Read one approved markdown file into heading sections."""

    meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    product_id = meta.get("id") or path.stem
    first_heading = next(
        (title for title, _content in split_sections(body) if title != "Overview"),
        path.stem.replace("_", " ").title(),
    )
    product_name = meta.get("name") or first_heading
    document = meta.get("document") or meta.get("title") or f"{product_name} Brochure"
    category = meta.get("category") or "General"
    summary = meta.get("summary") or ""
    return [
        MarkdownSection(
            product_id=product_id,
            product_name=product_name,
            category=category,
            summary=summary,
            document=document,
            filename=path.name,
            section=section_name,
            content=content,
        )
        for section_name, content in split_sections(body)
    ]


def load_all_markdown(approved_dir: Path) -> list[MarkdownSection]:
    """Load every `*.md` file in the approved corpus."""

    if not approved_dir.is_dir():
        return []
    sections: list[MarkdownSection] = []
    for path in sorted(approved_dir.glob("*.md")):
        sections.extend(load_markdown_file(path))
    return sections
