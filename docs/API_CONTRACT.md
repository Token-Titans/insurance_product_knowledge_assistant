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
    "id": "product_a",
    "name": "Product A",
    "category": "Health"
  }
]
```

`GET /products/{id}`

**Status: IMPLEMENTED**

Response:

```json
{
  "id": "product_a",
  "name": "Product A",
  "summary": "...",
  "benefits": ["..."]
}
```

Unknown ids return HTTP 404 with `PRODUCT_NOT_FOUND`.

`GET /products/{id}/suggested-questions`

**Status: IMPLEMENTED**

Response:

```json
[
  {
    "id": "hospitalization",
    "title": "Hospitalization",
    "question": "What hospitalization benefits does Product A provide?"
  }
]
```

- `id` is a stable slug for the prompt card (`hospitalization`, `benefits`, `eligibility`, `coverage`, `conditions`, `exclusions`, `premium`, `riders`, or `overview`).
- `title` is a short English label for the card.
- `question` is the full prompt the agent can submit to `POST /assistant/ask`.
- Questions are generated only from headings that exist in that product's approved markdown. At most five questions are returned.
- Unknown ids return HTTP 404 with `PRODUCT_NOT_FOUND`.

## Ask Product Question

`POST /assistant/ask`

**Status: IMPLEMENTED**

Request:

```json
{
  "product_id": "product_a",
  "question": "What is the hospitalization benefit?"
}
```

- `product_id` is required and must match `knowledge/approved/{product_id}.pdf` or `{product_id}.md`. PDF is preferred when both exist and the PDF is readable.
- `question` is required (1–2000 characters).

Response:

```json
{
  "answer": "",
  "important_conditions": [],
  "exclusions": [],
  "source": {
    "document": "",
    "file": "",
    "section": "",
    "page": null
  },
  "confidence": 0.0
}
```

`source` is copied from a retrieved markdown section or PDF page and is never invented. `page` is set for PDF chunks and omitted/null for markdown. When nothing relevant is found, `source` fields are empty strings and `confidence` is `0.0`. When `OPENAI_API_KEY` is unset, the API still answers from retrieved sections.

## Follow-up reminder

`POST /assistant/follow-up`

**Status: IMPLEMENTED**

After a grounded ask, the agent can schedule a reminder. FastAPI does not send email and does not wait. It posts to `N8N_WEBHOOK_URL`; n8n waits until `follow_up_date` and emails the agent.

Request:

```json
{
  "customer_name": "Aung Aung",
  "product_id": "dai-ichi-life-pro",
  "follow_up_date": "2026-09-05",
  "note": "Call back about the Life Pro living benefit."
}
```

- `customer_name` is required (1–120 characters).
- `product_id` must match an approved product (`PRODUCT_NOT_FOUND` if unknown).
- `follow_up_date` is `YYYY-MM-DD` and must be today or later.
- `note` is required (1–2000 characters).

n8n webhook body:

```json
{
  "customer_name": "Aung Aung",
  "product": "Dai-ichi Life Pro",
  "product_id": "dai-ichi-life-pro",
  "follow_up_date": "2026-09-05",
  "note": "Call back about the Life Pro living benefit."
}
```

n8n must respond to the webhook immediately, then Wait until `follow_up_date`, then send the reminder email. If n8n waits before responding, the API times out.

Response:

```json
{
  "status": "scheduled",
  "customer_name": "Aung Aung",
  "product": "Dai-ichi Life Pro",
  "follow_up_date": "2026-09-05"
}
```

When `N8N_WEBHOOK_URL` is empty or n8n is unreachable: HTTP 503 `AUTOMATION_UNAVAILABLE`. When n8n returns 4xx: HTTP 400 `FOLLOW_UP_REFUSED`.

Swagger UI: `http://localhost:8000/docs`

## Compare Products

`POST /assistant/compare`

**Status: IMPLEMENTED**

Request matches the frontend compare composer:

```json
{
  "question": "What are the key benefits, conditions, and exclusions?",
  "left_product_id": "dai_ichi_life_pro",
  "right_product_id": "dai_ichi_guard"
}
```

- `question` is required (1–2000 characters).
- `left_product_id` and `right_product_id` are required, must be different, and must match approved product files.
- The same handlers are served under `/api/v1/assistant/compare`.

Response:

```json
{
  "left": {
    "answer": "",
    "important_conditions": [],
    "exclusions": [],
    "source": {
      "document": "",
      "file": "",
      "section": "",
      "page": null
    },
    "confidence": 0.0
  },
  "right": {
    "answer": "",
    "important_conditions": [],
    "exclusions": [],
    "source": {
      "document": "",
      "file": "",
      "section": "",
      "page": null
    },
    "confidence": 0.0
  }
}
```

Each column is a grounded `POST /assistant/ask` result for that product only. Sources are never mixed. Identical product ids return HTTP 422 `INVALID_REQUEST`. Unknown ids return HTTP 404 `PRODUCT_NOT_FOUND`.

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
- `AUTOMATION_UNAVAILABLE` — n8n webhook is not configured or unreachable (HTTP 503).
- `FOLLOW_UP_REFUSED` — n8n rejected the follow-up payload (HTTP 400).
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
