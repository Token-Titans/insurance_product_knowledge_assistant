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
        "Reads `knowledge/approved/{product_id}.md`, ranks the top 3 heading sections "
        "by keyword overlap, then asks OpenAI. `source` is copied from a retrieved "
        "section and is never invented. When `OPENAI_API_KEY` is unset, the API returns "
        "an extractive answer from those sections."
    ),
)
async def ask(
    payload: AskRequest,
    settings: Settings = Depends(get_settings),
) -> AssistantResponse:
    """Answer a sales-agent product question from approved documents."""

    return await ask_product_question(payload.product_id, payload.question, settings)
