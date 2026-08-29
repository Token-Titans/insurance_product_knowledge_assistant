"""Assistant product-knowledge routes."""

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.models.assistant import (
    AskRequest,
    AssistantResponse,
    CompareRequest,
    CompareResponse,
    FollowUpRequest,
    FollowUpResponse,
)
from app.services.assistant import ask_product_question, compare_products
from app.services.follow_up import send_follow_up

router = APIRouter(prefix="/assistant", tags=["Assistant"])


@router.post(
    "/ask",
    response_model=AssistantResponse,
    response_model_exclude_none=True,
    summary="Ask a product-knowledge question",
    description=(
        "Reads `knowledge/approved/{product_id}.pdf` when present, otherwise "
        "`{product_id}.md`. Ranks the top 3 chunks by keyword overlap, then asks OpenAI. "
        "`source` is copied from a retrieved section (optional `page` for PDFs) and is "
        "never invented. Unreadable PDFs fall back to markdown."
    ),
)
async def ask(
    payload: AskRequest,
    settings: Settings = Depends(get_settings),
) -> AssistantResponse:
    """Answer a sales-agent product question from approved documents."""

    return await ask_product_question(payload.product_id, payload.question, settings)


@router.post(
    "/compare",
    response_model=CompareResponse,
    response_model_exclude_none=True,
    summary="Compare two approved products",
    description=(
        "Runs the same grounded ask against `left_product_id` and `right_product_id`. "
        "Each column is retrieved and cited independently. The products must be different. "
        "Unknown ids return HTTP 404 with `PRODUCT_NOT_FOUND`."
    ),
    responses={
        404: {
            "description": "Unknown product id",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "code": "PRODUCT_NOT_FOUND",
                            "message": "Unknown product 'missing-id'.",
                        }
                    }
                }
            },
        }
    },
)
async def compare(
    payload: CompareRequest,
    settings: Settings = Depends(get_settings),
) -> CompareResponse:
    """Compare one question across two approved products."""

    return await compare_products(
        payload.left_product_id,
        payload.right_product_id,
        payload.question,
        settings,
    )


@router.post(
    "/follow-up",
    response_model=FollowUpResponse,
    summary="Schedule a follow-up reminder",
    description=(
        "Forwards customer_name, product, follow_up_date, and note to the n8n "
        "webhook. n8n waits until the date and emails the sales agent. FastAPI "
        "does not send email and does not wait for the reminder."
    ),
)
async def follow_up(
    payload: FollowUpRequest,
    settings: Settings = Depends(get_settings),
) -> FollowUpResponse:
    """Hand a scheduled follow-up to n8n."""

    return await send_follow_up(payload, settings)
