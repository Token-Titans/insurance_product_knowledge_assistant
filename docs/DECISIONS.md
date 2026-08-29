# Architectural Decisions

## Accepted

### 001 — Four-hour foundation and strict scope

InsureAssist targets insurance sales agents and product knowledge only. The initial commit contains runnable scaffolds and governance, with no product features. Demo reliability and grounded answers take priority over optional features and architectural elegance.

### 002 — Monorepo with clear ownership

Use `apps/web/` for the web app, `services/api/` for the backend, and `docs/` for shared contracts. Do not create unnecessary shared packages. Ownership and coordination rules are defined in `docs/DEVELOPER_OWNERSHIP.md`.

### 003 — Web and API stack

Use Next.js App Router, TypeScript, and Tailwind for the web app; use FastAPI, Pydantic, and Uvicorn for the API. Keep browser code free of secrets and business logic.

### 004 — Backend owns product logic

FastAPI will own retrieval, prompts, AI calls, document processing, product logic, secrets, and n8n integration. n8n may own optional follow-up automation but never core product-knowledge logic.

### 005 — Contract-first integration

All API routes use `/api/v1`. Foundation implemented only `GET /api/v1/health`. `POST /api/v1/assistant/ask` is now implemented. Compare remains planned. Changes follow `docs/API_CONTRACT.md`.

### 006 — Approved documents are authoritative

Future answers must be grounded in approved product documents, include relevant conditions and sources, and acknowledge unsupported information. General model knowledge is not a substitute for product sources.

### 007 — Simple hackathon infrastructure

Target Netlify for Next.js and Python-capable hosting for FastAPI. Avoid authentication, complex databases, microservices, Docker, message brokers, and speculative infrastructure unless explicitly requested.

### 008 — OpenAI generation with keyword retrieval

Ask answers are grounded in approved markdown under `services/api/app/knowledge/approved/`. Retrieval is section-level keyword overlap (no vector database). Generation uses OpenAI Chat Completions (`gpt-4o-mini` by default) when `OPENAI_API_KEY` is set server-side. If the key is missing or the provider call fails, the API returns an extractive answer from retrieved sections so the core flow still works.

## Pending feature decisions

- Document extraction for non-markdown sources (PDF) if the approved corpus format changes.
- Hosting provider for FastAPI.
- Whether the should-have n8n follow-up is attempted.

Record an agreed decision here before introducing a new architectural commitment.
