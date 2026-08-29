# API Contract

Base path: `/api/v1`

`GET /api/v1/health` and `POST /api/v1/assistant/ask` are implemented. Compare remains planned.

## Health

`GET /api/v1/health`

**Status: IMPLEMENTED**

Response:

```json
{
  "status": "ok",
  "service": "insureassist-api"
}
```

## Ask Product Question

`POST /api/v1/assistant/ask`

**Status: IMPLEMENTED**

Request:

```json
{
  "question": "What is the hospitalization benefit?",
  "product_ids": ["product-a"]
}
```

- `question` is required (1–2000 characters).
- `product_ids` is optional. Supported values: `product-a`, `product-b`. Unknown IDs return `UNKNOWN_PRODUCT`. When omitted, approved documents for all supported products are searched.

Response:

```json
{
  "answer": "Product A provides...",
  "important_points": ["..."],
  "conditions": ["..."],
  "sources": [
    {
      "document": "Product A Brochure",
      "section": "Hospital Benefits"
    }
  ],
  "confidence": "grounded"
}
```

`confidence` is `"grounded"` when approved sources support the answer, or `"unavailable"` when they do not. Unavailable information is still HTTP 200 with a safe message and empty `sources`.

When `OPENAI_API_KEY` is not set, the API still answers from retrieved approved sections (extractive fallback). With a key, the backend calls OpenAI and validates the structured result before returning it.

## Compare Products

`POST /api/v1/assistant/compare`

**Status: PLANNED / SHOULD HAVE**

The request and response schema will be agreed before implementation. Do not implement this endpoint from assumptions.

## Standard error

Product endpoints use:

```json
{
  "detail": {
    "code": "ERROR_CODE",
    "message": "Human-readable message"
  }
}
```

Ask endpoint error codes:

- `INVALID_REQUEST` — missing or invalid body (HTTP 400 or 422).
- `UNKNOWN_PRODUCT` — `product_ids` contains an unsupported id (HTTP 400).
- `HTTP_ERROR` — other HTTP errors.

## API governance

For every API change:

1. Discuss the change with the Integration Lead.
2. Update `docs/API_CONTRACT.md`.
3. Update the backend.
4. Update the frontend.
5. Test integration.
6. Commit clearly.

Never silently change a request, response, path, or error shape. Coordinate with Developer 4 before changing this contract.
