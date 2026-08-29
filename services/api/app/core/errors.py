"""Stable API error helpers. Never include credentials or stack traces."""

from fastapi import HTTPException, status


class ApiError(HTTPException):
    """HTTP error with the documented `{detail: {code, message}}` shape."""

    def __init__(self, status_code: int, code: str, message: str) -> None:
        super().__init__(
            status_code=status_code,
            detail={"code": code, "message": message},
        )


def invalid_request(message: str) -> ApiError:
    """Return HTTP 400 for a semantically invalid request."""

    return ApiError(status.HTTP_400_BAD_REQUEST, "INVALID_REQUEST", message)


def product_not_found(product_id: str) -> ApiError:
    """Return HTTP 404 when a product id is not in the approved corpus."""

    return ApiError(
        status.HTTP_404_NOT_FOUND,
        "PRODUCT_NOT_FOUND",
        f"Unknown product '{product_id}'.",
    )


def automation_unavailable() -> ApiError:
    """Return HTTP 503 when the n8n webhook is missing or unreachable."""

    return ApiError(
        status.HTTP_503_SERVICE_UNAVAILABLE,
        "AUTOMATION_UNAVAILABLE",
        "Follow-up service is not configured.",
    )


def follow_up_refused(
    message: str = "The follow-up could not be scheduled.",
) -> ApiError:
    """Return HTTP 400 when n8n refuses the follow-up payload."""

    return ApiError(status.HTTP_400_BAD_REQUEST, "FOLLOW_UP_REFUSED", message)
