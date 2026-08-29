# Architecture

## Current implementation

```text
Next.js  ── HTTP + CORS ──>  FastAPI (/docs Swagger)
                                  │
                    GET  /health
                    GET  /products
                    GET  /products/{id}
                    POST /assistant/ask
                    (aliases under /api/v1)
                                  │
                                  ▼
                         Approved markdown
                         keyword retrieval (top 3)
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
              OpenAI SDK (if key)        Extractive fallback
```

- `apps/web/`: Next.js App Router scaffold (frontend unchanged by this backend work).
- `services/api/`: FastAPI with health and ask. Product facts come only from `app/knowledge/approved/`.
- Compare, n8n, persistence, and authentication are not implemented.

## Planned MVP

```text
                  SALES AGENT
                       │
                       ▼
                  Next.js Web
                  + Tailwind
                       │
                     HTTPS
                       │
                       ▼
                    FastAPI
                       │
             ┌─────────┼──────────┐
             ▼         ▼          ▼
          Product   Knowledge   Future
          Service   Retrieval     n8n
                       │
                       ▼
                    LLM API
                       │
                       ▼
              Grounded Response
                  + Sources
```

Planned responsibilities:

- Next.js presents the sales-agent workflow and calls only the documented API.
- FastAPI owns validation, product logic, retrieval, prompts, AI integration, document processing, server-side secrets, and automation requests.
- Approved product documents are the source of truth.
- The LLM produces a grounded response from retrieved knowledge and does not replace source documents.
- n8n may execute optional email, reminder, or sales follow-up workflows. It must not contain core product-knowledge logic.

Ask uses OpenAI when `OPENAI_API_KEY` is set (see `docs/DECISIONS.md` 008). Compare and n8n remain undecided.

## Deployment targets

- Next.js → Netlify.
- FastAPI → Python-capable hosting.
- n8n → n8n Cloud or the hackathon environment.

## Constraints

Keep the hackathon architecture simple. Do not introduce microservices, complex databases, message brokers, Kafka, Redis, Celery, Docker, authentication, or speculative infrastructure unless explicitly requested. Update this document when an agreed architecture decision changes.
