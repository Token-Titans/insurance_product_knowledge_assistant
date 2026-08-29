# API Contract

Base path: `/api/v1`

Only the health endpoint is implemented. All other endpoints are documentation for planned product work and must not be treated as available.

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

**Status: PLANNED**

Future example request:

```json
{
  "question": "What is the hospitalization benefit?",
  "product_ids": ["product-a"]
}
```

Future example response:

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

## Compare Products

`POST /api/v1/assistant/compare`

**Status: PLANNED / SHOULD HAVE**

The request and response schema will be agreed before implementation. Do not implement this endpoint from assumptions.

## Standard error

Planned product endpoints use:

```json
{
  "detail": {
    "code": "ERROR_CODE",
    "message": "Human-readable message"
  }
}
```

## API governance

For every API change:

1. Discuss the change with the Integration Lead.
2. Update `docs/API_CONTRACT.md`.
3. Update the backend.
4. Update the frontend.
5. Test integration.
6. Commit clearly.

Never silently change a request, response, path, or error shape. A planned example does not authorize implementation.
