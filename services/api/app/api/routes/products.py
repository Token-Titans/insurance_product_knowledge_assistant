"""Product catalog routes backed by approved markdown."""

from fastapi import APIRouter

from app.models.assistant import ProductDetail, ProductSummary
from app.services.products import get_product, list_products

router = APIRouter(prefix="/products", tags=["Products"])


@router.get(
    "",
    response_model=list[ProductSummary],
    summary="List approved products",
    description="Returns one card per approved markdown product. Metadata comes from file frontmatter, or is inferred from the filename and first heading.",
)
async def products() -> list[ProductSummary]:
    """List products discovered in the approved corpus."""

    return list_products()


@router.get(
    "/{id}",
    response_model=ProductDetail,
    summary="Get one approved product",
    description="Returns summary and benefit bullets for a single product id such as `family-care`.",
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
async def product_detail(id: str) -> ProductDetail:
    """Return one product or 404 if it is not in the approved corpus."""

    return get_product(id)
