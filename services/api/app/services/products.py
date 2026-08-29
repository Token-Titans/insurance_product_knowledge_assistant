"""Product catalog derived from approved markdown metadata."""

from app.core.errors import product_not_found
from app.models.assistant import ProductDetail, ProductSummary, SuggestedQuestion
from app.services.retrieve import DocumentSection, load_documents

_MAX_SUGGESTIONS = 5
_FALLBACK_QUESTION = "What should a sales agent know about {name}?"
# heading (lowercase) -> (id, title, question template). Only headings that
# exist in the approved file are emitted, so prompts stay grounded.
_QUESTION_BY_HEADING: dict[str, tuple[str, str, str]] = {
    "hospitalization benefits": (
        "hospitalization",
        "Hospitalization",
        "What hospitalization benefits does {name} provide?",
    ),
    "benefits": (
        "benefits",
        "Benefits",
        "What benefits does {name} provide?",
    ),
    "eligibility": (
        "eligibility",
        "Eligibility",
        "Who is eligible for {name}?",
    ),
    "coverage": (
        "coverage",
        "Coverage",
        "What does {name} cover?",
    ),
    "important conditions": (
        "conditions",
        "Conditions",
        "What important conditions apply to {name}?",
    ),
    "exclusions": (
        "exclusions",
        "Exclusions",
        "What exclusions apply to {name}?",
    ),
    "premium and payment": (
        "premium",
        "Premium",
        "How are premiums paid for {name}?",
    ),
    "riders and combinations": (
        "riders",
        "Riders",
        "Which riders can be added to {name}?",
    ),
}
_HEADING_ORDER = tuple(_QUESTION_BY_HEADING.keys())


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


def list_suggested_questions(product_id: str) -> list[SuggestedQuestion]:
    """Return sales prompts for headings that exist in the approved product file."""

    sections = _first_sections_by_product().get(product_id)
    if not sections:
        raise product_not_found(product_id)

    name = sections[0].product_name
    available = {section.section.lower() for section in sections}
    questions: list[SuggestedQuestion] = []
    for heading in _HEADING_ORDER:
        if heading not in available:
            continue
        question_id, title, template = _QUESTION_BY_HEADING[heading]
        questions.append(
            SuggestedQuestion(
                id=question_id,
                title=title,
                question=template.format(name=name),
            )
        )
        if len(questions) >= _MAX_SUGGESTIONS:
            break

    if questions:
        return questions
    return [
        SuggestedQuestion(
            id="overview",
            title="Overview",
            question=_FALLBACK_QUESTION.format(name=name),
        )
    ]
