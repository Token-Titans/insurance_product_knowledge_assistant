"""Product catalog derived from approved markdown metadata."""

from app.core.errors import product_not_found
from app.models.assistant import ProductDetail, ProductSummary
from app.services.retrieve import DocumentSection, load_documents


def _first_sections_by_product() -> dict[str, list[DocumentSection]]:
    grouped: dict[str, list[DocumentSection]] = {}
    for section in load_documents():
        grouped.setdefault(section.product_id, []).append(section)
    return grouped


def _benefits_from(sections: list[DocumentSection]) -> list[str]:
    benefits: list[str] = []
    for section in sections:
        if "benefit" not in section.section.lower():
            continue
        for line in section.content.splitlines():
            stripped = line.strip()
            if stripped.startswith("- "):
                benefits.append(stripped[2:].strip())
    return benefits


def list_products() -> list[ProductSummary]:
    """Return one summary row per approved product file."""

    products: list[ProductSummary] = []
    seen: set[str] = set()
    for section in load_documents():
        if section.product_id in seen:
            continue
        seen.add(section.product_id)
        products.append(
            ProductSummary(
                id=section.product_id,
                name=section.product_name,
                category=section.category,
            )
        )
    return products


def get_product(product_id: str) -> ProductDetail:
    """Return detail for one product or raise PRODUCT_NOT_FOUND."""

    sections = _first_sections_by_product().get(product_id)
    if not sections:
        raise product_not_found(product_id)
    head = sections[0]
    summary = head.summary.strip()
    if not summary:
        overview = next(
            (item.content for item in sections if item.section.lower() == "overview"),
            sections[0].content,
        )
        summary = " ".join(overview.split())[:280]
    return ProductDetail(
        id=head.product_id,
        name=head.product_name,
        summary=summary,
        benefits=_benefits_from(sections),
    )
