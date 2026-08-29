"""Assistant product-knowledge routes."""

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.models.assistant import AskRequest, AskResponse
from app.services.assistant import ask_product_question

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.post("/ask", response_model=AskResponse)
def ask(
    payload: AskRequest,
    settings: Settings = Depends(get_settings),
) -> AskResponse:
    """Answer a sales-agent product question from approved documents."""

    return ask_product_question(payload, settings)
