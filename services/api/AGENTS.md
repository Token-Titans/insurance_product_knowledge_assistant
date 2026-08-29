# InsureAssist API

## Scope

- Keep all API work inside `services/api`.
- Preserve the `/api/v1` route prefix.
- Keep configuration in `app/core/config.py` and load values from environment variables.
- Define Pydantic response models for API responses.

## Commands

- Run locally: `uvicorn app.main:app --reload`
- Run tests: `pytest`

## Implemented

- `GET /api/v1/health`
- `POST /api/v1/assistant/ask` — grounded product answers from approved markdown in
  `app/knowledge/approved/`. OpenAI is used when `OPENAI_API_KEY` is set; otherwise
  the service returns an extractive answer from retrieved sections.

## Boundaries

- Do not modify `apps/web`.
- Do not implement compare, n8n, authentication, or databases unless explicitly requested.
- Keep the API key server-side in `.env`. Never commit secrets.
