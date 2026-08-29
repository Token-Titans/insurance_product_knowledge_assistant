# InsureAssist API

## Scope

- Keep all API work inside `services/api`.
- Canonical routes: `/health`, `/products`, `/products/{id}`, `/assistant/ask`.
- The same handlers are mounted under `/api/v1` for compatibility.
- Keep configuration in `app/core/config.py` and load values from environment variables.
- Define Pydantic response models for API responses.
- Swagger UI is at `/docs`.

## Commands

- Run locally: `uvicorn app.main:app --reload`
- Run tests: `pytest`

## Implemented

- `GET /health`
- `GET /products` and `GET /products/{id}`
- `POST /assistant/ask` — grounded answers from `app/knowledge/approved/`.
  OpenAI is used when `OPENAI_API_KEY` is set; otherwise extractive retrieval.

## Boundaries

- Do not modify `apps/web`.
- Do not implement compare, n8n, authentication, or databases unless explicitly requested.
- Keep the API key server-side in `.env`. Never commit secrets.
