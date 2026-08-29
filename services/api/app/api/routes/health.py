"""Health-check route."""

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    """Health-check response body."""

    status: Literal["ok"]
    service: Literal["insureassist-api"]


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Return the API's current health status."""

    return HealthResponse(status="ok", service="insureassist-api")
