"""Assistant product-knowledge routes."""

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.models.assistant import AskRequest, AssistantResponse
from app.services.assistant import ask_product_question

router = APIRouter(prefix="/assistant", tags=["Assistant"])


@router.post(
    "/ask",
    response_model=AssistantResponse,
    response_model_exclude_none=True,
    summary="Ask a product-knowledge question",
    description=(
        "Retrieves the top matching approved markdown sections, then generates a grounded "
        "answer. Citations always come from retrieved files. When `OPENAI_API_KEY` is "
        "unset, the API returns an extractive answer from those sections."
    ),
)
async def ask(
    payload: AskRequest,
    settings: Settings = Depends(get_settings),
) -> AssistantResponse:
    """Answer a sales-agent product question from approved documents."""

    return await ask_product_question(payload.question, settings)
