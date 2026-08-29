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
    """Compact product card for GET /products."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"id": "product_a", "name": "Product A", "category": "Health"}
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
                    "id": "product_a",
                    "name": "Product A",
                    "summary": "Hospitalisation plan for working adults.",
                    "benefits": ["Room and board up to RM300 per day"],
                }
            ]
        }
    )

    id: str
    name: str
    summary: str
    benefits: list[str]


class SourceReference(BaseModel):
    """Single citation copied from a retrieved markdown section. Never fabricated."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "document": "Product A Brochure",
                    "file": "product_a.md",
                    "section": "Hospitalization Benefits",
                }
            ]
        }
    )

    document: str = ""
    file: str = ""
    section: str = ""


class AskRequest(BaseModel):
    """Ask a question about one approved product."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "product_id": "product_a",
                    "question": "What is the hospitalization benefit?",
                }
            ]
        }
    )

    product_id: str = Field(..., min_length=1, max_length=64, examples=["product_a"])
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        examples=["What is the hospitalization benefit?"],
    )


class AssistantResponse(BaseModel):
    """Grounded product answer with conditions, exclusions, and one source."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "answer": (
                        "Product A pays room and board up to RM300 per day, ICU up to "
                        "RM600 per day, and hospital miscellaneous charges up to RM15,000 per admission."
                    ),
                    "important_conditions": [
                        "30-day waiting period except accidents.",
                        "Pre-authorisation required for planned admissions.",
                    ],
                    "exclusions": [
                        "Undisclosed pre-existing conditions are not covered.",
                        "Cosmetic procedures are not covered.",
                    ],
                    "source": {
                        "document": "Product A Brochure",
                        "file": "product_a.md",
                        "section": "Hospitalization Benefits",
                    },
                    "confidence": 0.82,
                }
            ]
        }
    )

    answer: str
    important_conditions: list[str]
    exclusions: list[str]
    source: SourceReference
    confidence: float = Field(..., ge=0.0, le=1.0)
