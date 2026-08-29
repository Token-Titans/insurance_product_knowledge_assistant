# Architecture

## Current foundation

```text
Next.js scaffold  ── future HTTP ──>  FastAPI scaffold
                                          │
                                          └── GET /api/v1/health
```

- `apps/web/`: runnable Next.js App Router scaffold with TypeScript and Tailwind.
- `services/api/`: runnable FastAPI scaffold with explicit CORS and configuration.
- No AI, retrieval, document processing, persistence, automation, or product endpoints are implemented.
- No shared package is needed at this stage.

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

The exact model and retrieval implementation will be decided during feature development; no RAG implementation is selected by this document.

## Deployment targets

- Next.js → Netlify.
- FastAPI → Python-capable hosting.
- n8n → n8n Cloud or the hackathon environment.

## Constraints

Keep the hackathon architecture simple. Do not introduce microservices, complex databases, message brokers, Kafka, Redis, Celery, Docker, authentication, or speculative infrastructure unless explicitly requested. Update this document when an agreed architecture decision changes.
