# InsureAssist API

## Scope

- Keep all API work inside `services/api`.
- Preserve the `/api/v1` route prefix.
- Keep configuration in `app/core/config.py` and load values from environment variables.
- Define Pydantic response models for API responses.

## Commands

- Run locally: `uvicorn app.main:app --reload`
- Run tests: `pytest`

## Current boundaries

This foundation contains only the health endpoint. Do not add AI, retrieval,
document, ask/compare, automation, authentication, database, Docker, or product
features without an explicit request.
