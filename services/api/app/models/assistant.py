"""Pydantic API models. Response shapes are frozen for the frontend."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    """Liveness payload for load balancers and the web app."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"status": "ok", "service": "insurance-assistant"}]
        }
    )

    status: Literal["ok"] = "ok"
    service: Literal["insurance-assistant"] = "insurance-assistant"


class ProductSummary(BaseModel):
    """Compact product card used in lists and assistant recommendations."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"id": "family-care", "name": "Family Care", "category": "Health"}
            ]
        }
    )

    id: str
    name: str
    category: str | None = None


class ProductDetail(BaseModel):
    """Product page payload derived from an approved markdown file."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "family-care",
                    "name": "Family Care",
                    "summary": "Hospital and outpatient cover for working adults and their families.",
                    "benefits": [
                        "Room and board up to RM300 per day",
                        "Outpatient GP visits up to RM50 per visit",
                    ],
                }
            ]
        }
    )

    id: str
    name: str
    summary: str
    benefits: list[str]


class SourceReference(BaseModel):
    """Citation pointing at an approved markdown section. Never fabricated."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Family Care Brochure",
                    "file": "family_care.md",
                    "section": "Eligibility",
                }
            ]
        }
    )

    title: str
    file: str
    section: str


class AskRequest(BaseModel):
    """Natural-language product-knowledge question from a sales agent."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"question": "I am 30 years old. Which insurance is suitable?"}
            ]
        }
    )

    question: str = Field(..., min_length=1, max_length=2000, examples=[
        "I am 30 years old. Which insurance is suitable?"
    ])


class AssistantResponse(BaseModel):
    """Grounded answer with citations and optional product recommendations."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "answer": (
                        "Family Care is suitable for a 30-year-old working adult. "
                        "Eligibility is ages 18 to 60 at policy start."
                    ),
                    "sources": [
                        {
                            "title": "Family Care Brochure",
                            "file": "family_care.md",
                            "section": "Eligibility",
                        }
                    ],
                    "recommended_products": [
                        {"id": "family-care", "name": "Family Care"}
                    ],
                }
            ]
        }
    )

    answer: str
    sources: list[SourceReference]
    recommended_products: list[ProductSummary]
