# API Contract

Frozen frontend contract. Do not change request, response, path, or error shapes silently.

Unprefixed paths are canonical. The same handlers are also served under `/api/v1`.

## Health

`GET /health`

**Status: IMPLEMENTED**

Response:

```json
{
  "status": "ok",
  "service": "insurance-assistant"
}
```

## Products

`GET /products`

**Status: IMPLEMENTED**

Response:

```json
[
  {
    "id": "family-care",
    "name": "Family Care",
    "category": "Health"
  }
]
```

`GET /products/{id}`

**Status: IMPLEMENTED**

Response:

```json
{
  "id": "family-care",
  "name": "Family Care",
  "summary": "...",
  "benefits": ["..."]
}
```

Unknown ids return HTTP 404 with `PRODUCT_NOT_FOUND`.

## Ask Product Question

`POST /assistant/ask`

**Status: IMPLEMENTED**

Request:

```json
{
  "question": "I am 30 years old. Which insurance is suitable?"
}
```

- `question` is required (1–2000 characters).

Response:

```json
{
  "answer": "Recommended product is Family Care...",
  "sources": [
    {
      "title": "Family Care Brochure",
      "file": "family_care.md",
      "section": "Eligibility"
    }
  ],
  "recommended_products": [
    {
      "id": "family-care",
      "name": "Family Care"
    }
  ]
}
```

`sources` are copied from retrieved markdown only. They are never invented. When `OPENAI_API_KEY` is unset, the API still answers from retrieved sections.

Swagger UI: `http://localhost:8000/docs`

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

Error codes:

- `INVALID_REQUEST` — missing or invalid body (HTTP 400 or 422).
- `PRODUCT_NOT_FOUND` — unknown product id (HTTP 404).
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
