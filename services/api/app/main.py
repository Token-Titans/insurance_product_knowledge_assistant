"""FastAPI application entry point."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routes import api_router
from app.core.config import get_settings

settings = get_settings()

_DESCRIPTION = """
InsureAssist backend for insurance **sales agents**.

Answers come only from approved markdown in `app/knowledge/approved/`.
The model must not invent benefits, limits, or eligibility rules.

**Frozen frontend contract**

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Liveness |
| `GET` | `/products` | Product list |
| `GET` | `/products/{id}` | Product detail |
| `POST` | `/assistant/ask` | Grounded Q&A |
| `POST` | `/assistant/follow-up` | Schedule n8n reminder |

The same routes are also mounted under `/api/v1` for the repository convention.
"""

app = FastAPI(
    title="Insurance Product Knowledge Assistant",
    description=_DESCRIPTION,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {"name": "Health", "description": "Liveness checks."},
        {"name": "Products", "description": "Approved product catalog from markdown."},
        {
            "name": "Assistant",
            "description": "Grounded product-knowledge questions with source citations.",
        },
    ],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
app.include_router(api_router, prefix="/api/v1", include_in_schema=False)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    _request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Return documented `{detail: {code, message}}` errors."""

    if isinstance(exc.detail, dict) and "code" in exc.detail:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": {
                "code": "HTTP_ERROR",
                "message": str(exc.detail),
            }
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Map request validation failures to the documented error shape."""

    first = exc.errors()[0] if exc.errors() else {}
    location = ".".join(str(part) for part in first.get("loc", []) if part != "body")
    message = str(first.get("msg", "Invalid request"))
    if location:
        message = f"{location}: {message}"
    return JSONResponse(
        status_code=422,
        content={
            "detail": {
                "code": "INVALID_REQUEST",
                "message": message,
            }
        },
    )
