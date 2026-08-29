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
    return ApiError(status.HTTP_400_BAD_REQUEST, "INVALID_REQUEST", message)


def unknown_product(product_id: str) -> ApiError:
    return ApiError(
        status.HTTP_400_BAD_REQUEST,
        "UNKNOWN_PRODUCT",
        f"Unknown product_id '{product_id}'. Use a supported product such as product-a or product-b.",
    )
