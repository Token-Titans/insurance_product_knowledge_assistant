"""Application models package."""

from app.models.assistant import (
    AskRequest,
    AssistantResponse,
    HealthResponse,
    ProductDetail,
    ProductSummary,
    SourceReference,
    SuggestedQuestion,
)

__all__ = [
    "AskRequest",
    "AssistantResponse",
    "HealthResponse",
    "ProductDetail",
    "ProductSummary",
    "SourceReference",
    "SuggestedQuestion",
]
