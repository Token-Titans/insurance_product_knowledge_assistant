"""POST follow-up reminders to the n8n webhook. No product-knowledge logic."""

from __future__ import annotations

import logging

import httpx

from app.core.errors import automation_unavailable, follow_up_refused

logger = logging.getLogger(__name__)


async def post_webhook(url: str, payload: dict[str, object]) -> None:
    """Send JSON to n8n and return after the webhook ACK.

    n8n must respond immediately, then Wait until follow_up_date, then email.
    Do not wait in FastAPI for the reminder to send.
    """

    target = url.strip()
    if not target:
        raise automation_unavailable()

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(target, json=payload)
    except httpx.HTTPError:
        logger.warning("n8n webhook request failed")
        raise automation_unavailable() from None

    if response.status_code >= 500:
        logger.warning("n8n webhook returned %s", response.status_code)
        raise automation_unavailable()
    if response.status_code >= 400:
        raise follow_up_refused()
