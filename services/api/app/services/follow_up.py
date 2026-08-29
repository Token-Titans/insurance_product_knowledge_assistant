"""Schedule a sales follow-up reminder. n8n waits and sends the email."""

from datetime import date

from app.core.config import Settings
from app.core.errors import invalid_request
from app.models.assistant import FollowUpRequest, FollowUpResponse
from app.services.n8n import post_webhook
from app.services.products import get_product


def _n8n_payload(request: FollowUpRequest, product_name: str) -> dict[str, object]:
    return {
        "customer_name": request.customer_name.strip(),
        "product": product_name,
        "product_id": request.product_id.strip(),
        "follow_up_date": request.follow_up_date.isoformat(),
        "note": request.note.strip(),
    }


async def send_follow_up(request: FollowUpRequest, settings: Settings) -> FollowUpResponse:
    """Validate the product, then hand the reminder to n8n. Do not wait for the send."""

    customer_name = request.customer_name.strip()
    note = request.note.strip()
    if not customer_name:
        raise invalid_request("customer_name must not be empty")
    if not note:
        raise invalid_request("note must not be empty")
    if request.follow_up_date < date.today():
        raise invalid_request("follow_up_date must be today or later")

    product = get_product(request.product_id)
    await post_webhook(settings.n8n_webhook_url, _n8n_payload(request, product.name))
    return FollowUpResponse(
        status="scheduled",
        customer_name=customer_name,
        product=product.name,
        follow_up_date=request.follow_up_date,
    )
