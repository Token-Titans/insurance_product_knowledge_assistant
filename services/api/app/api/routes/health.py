"""Health-check route."""

from fastapi import APIRouter

from app.models.assistant import HealthResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Service health",
    description="Returns a static liveness payload. Used by local checks and future hosting probes.",
)
async def health() -> HealthResponse:
    """Return the API's current health status."""

    return HealthResponse(status="ok", service="insurance-assistant")
