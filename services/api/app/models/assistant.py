"""Request and response models for the assistant ask endpoint."""

from typing import Literal

from pydantic import BaseModel, Field


class SourceReference(BaseModel):
    """Citation a sales agent can verify in an approved document."""

    document: str
    section: str


class AskRequest(BaseModel):
    """Ask a product-knowledge question about approved documents."""

    question: str = Field(..., min_length=1, max_length=2000)
    product_ids: list[str] = Field(default_factory=list)


class AskResponse(BaseModel):
    """Grounded product-knowledge answer for a sales agent."""

    answer: str
    important_points: list[str]
    conditions: list[str]
    sources: list[SourceReference]
    confidence: Literal["grounded", "unavailable"]
