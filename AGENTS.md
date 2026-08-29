# InsureAssist Contributor Guide

InsureAssist is a four-hour hackathon project for **Reimagining Customer Engagement Through AI-Powered Digital Assistants**. Its only target user is an insurance sales agent. The product helps agents answer product-knowledge questions from approved insurance documents; it is not a generic chatbot or an insurance transaction, claims, underwriting, quotation, CRM, or customer-facing system.

Tagline: **Know the product. Answer with confidence.**

## Foundation boundary

This repository currently contains project scaffolding only. The only implemented API operation is `GET /api/v1/health`. Do not add product features during foundation work. In particular, do not add AI calls, RAG, embeddings, vector databases, document upload or extraction, question answering, comparison, n8n workflows, authentication, databases, chatbot screens, product UI, or fake product data.

## Architecture and authority

- `apps/web/`: Next.js App Router, TypeScript, and Tailwind; Vercel deployment.
- `services/api/`: FastAPI; future owner of business logic, retrieval, prompts, AI, document processing, secrets, and n8n calls.
- n8n may later own follow-up automation, never product-knowledge logic.
- `docs/PRODUCT_SCOPE.md` is the product boundary.
- `docs/API_CONTRACT.md` is the web/API interface authority.
- `docs/KNOWLEDGE_STRATEGY.md` governs future AI and knowledge behavior.
- `docs/ARCHITECTURE.md` distinguishes the current foundation from the planned MVP.

## Ownership

- Developer 1 — Web Frontend: `apps/web/**`
- Developer 2 — Backend/API: core areas under `services/api/**`
- Developer 3 — AI/Product Knowledge/Automation: future AI, knowledge, and automation service areas under `services/api/**`, coordinated with Developer 2
- Developer 4 — Integration/Product/Deployment: contracts, reviews, environments, deployment, end-to-end testing, demo, scope, and integration fixes

See `docs/DEVELOPER_OWNERSHIP.md`. Do not modify another developer's area without coordination.

## Mandatory workflow

Before modifying code:

1. Read root `AGENTS.md`.
2. Read `docs/PRODUCT_SCOPE.md`.
3. Identify the ownership area.
4. Read the nearest nested `AGENTS.md`.
5. If web/API communication changes, read `docs/API_CONTRACT.md`.
6. If knowledge/AI behavior changes, read `docs/KNOWLEDGE_STRATEGY.md`.
7. If architecture changes, read `docs/ARCHITECTURE.md`.
8. Modify only the smallest necessary scope.
9. Do not refactor unrelated working code.
10. Do not modify another developer's area without coordination.
11. Never silently change API contracts.
12. Run relevant checks after changes.

Do not develop directly on `main`. Pull before work, use the documented feature branch, make small commits, push frequently, open small PRs, and keep `main` runnable. Never commit secrets or add dependencies or infrastructure without a clear MVP need.

## Hackathon priorities

1. Working end-to-end demo
2. Accurate grounded product answers
3. Stable integration
4. Core user value
5. Reliability
6. UX polish
7. Optional features
8. Architectural perfection

Preserve working code. Near demo time, fix the critical flow instead of expanding scope.
