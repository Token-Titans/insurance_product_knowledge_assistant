"""Pydantic API models. Response shapes are frozen for the frontend."""

from datetime import date
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


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


class SuggestedQuestion(BaseModel):
    """One grounded sales prompt derived from an approved document heading."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "hospitalization",
                    "title": "Hospitalization",
                    "question": "What hospitalization benefits does Product A provide?",
                }
            ]
        }
    )

    id: str
    title: str
    question: str


class SourceReference(BaseModel):
    """Single citation copied from a retrieved markdown section. Never fabricated."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "document": "Product A Brochure",
                    "file": "product_a.pdf",
                    "section": "Page 2",
                    "page": 2,
                }
            ]
        }
    )

    document: str = ""
    file: str = ""
    section: str = ""
    page: int | None = None


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


class CompareRequest(BaseModel):
    """Compare the same question across two approved products."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "question": "What are the key benefits, conditions, and exclusions?",
                    "left_product_id": "dai_ichi_life_pro",
                    "right_product_id": "dai_ichi_guard",
                }
            ]
        }
    )

    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        examples=["What are the key benefits, conditions, and exclusions?"],
    )
    left_product_id: str = Field(
        ..., min_length=1, max_length=64, examples=["dai_ichi_life_pro"]
    )
    right_product_id: str = Field(
        ..., min_length=1, max_length=64, examples=["dai_ichi_guard"]
    )

    @model_validator(mode="after")
    def distinct_products(self) -> Self:
        if self.left_product_id.strip() == self.right_product_id.strip():
            raise ValueError("left_product_id and right_product_id must be different")
        return self


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
                        "page": None,
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


class CompareResponse(BaseModel):
    """Side-by-side grounded answers. Each column uses only that product's sources."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "left": {
                        "answer": "Dai-ichi Life Pro pays 100% of the sum insured on death or TPD.",
                        "important_conditions": [],
                        "exclusions": [],
                        "source": {
                            "document": "Dai-ichi Life Pro Product Guide",
                            "file": "dai_ichi_life_pro.md",
                            "section": "Benefits",
                            "page": None,
                        },
                        "confidence": 0.7,
                    },
                    "right": {
                        "answer": "Dai-ichi Guard adds a further 100% of the sum insured as a rider.",
                        "important_conditions": [],
                        "exclusions": [],
                        "source": {
                            "document": "Dai-ichi Guard Rider Guide",
                            "file": "dai_ichi_guard.md",
                            "section": "Benefits",
                            "page": None,
                        },
                        "confidence": 0.7,
                    },
                }
            ]
        }
    )

    left: AssistantResponse
    right: AssistantResponse


class FollowUpRequest(BaseModel):
    """Schedule a sales follow-up reminder through n8n."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "customer_name": "Aung Aung",
                    "product_id": "dai-ichi-life-pro",
                    "follow_up_date": "2026-09-05",
                    "note": "Call back about the Life Pro living benefit.",
                }
            ]
        }
    )

    customer_name: str = Field(..., min_length=1, max_length=120)
    product_id: str = Field(..., min_length=1, max_length=64)
    follow_up_date: date = Field(..., examples=["2026-09-05"])
    note: str = Field(..., min_length=1, max_length=2000)


class FollowUpResponse(BaseModel):
    """n8n accepted the reminder. Waiting and email happen in n8n."""

    status: Literal["scheduled"] = "scheduled"
    customer_name: str
    product: str
    follow_up_date: date
