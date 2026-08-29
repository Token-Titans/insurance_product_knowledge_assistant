# InsureAssist

**AI Insurance Product Knowledge Assistant for Sales Agents**

_Know the product. Answer with confidence._

InsureAssist is a foundation-only monorepo for a four-hour hackathon. The planned MVP helps insurance sales agents obtain clear, grounded answers from approved product documents, including important conditions and source references.

## Current status

- Next.js web scaffold in `apps/web/`
- FastAPI scaffold in `services/api/`
- Implemented API: `GET /api/v1/health`
- Planned only: question answering, comparison, retrieval, AI, document processing, and n8n automation

No product functionality should be inferred from the foundation scaffold.

## Repository map

```text
apps/web/       Next.js App Router, TypeScript, Tailwind
services/api/   FastAPI and future server-side product logic
docs/           Scope, contracts, architecture, workflow, and runbook
.cursor/rules/  Repository-specific Cursor guidance
```

## Start locally

Web:

```bash
cd apps/web
npm install
npm run dev
```

API:

```bash
cd services/api
python -m venv .venv
# Activate the virtual environment for your shell
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Copy each local `.env.example` to `.env` when configuration is needed. Never commit `.env` files.

## Validate

```bash
# apps/web
npm run lint
npm run build

# services/api
pytest
```

With the API running, `GET http://localhost:8000/api/v1/health` must return:

```json
{"status":"ok","service":"insureassist-api"}
```

## Before contributing

Read `AGENTS.md`, `docs/PRODUCT_SCOPE.md`, the nearest nested `AGENTS.md`, and any governing contract or strategy document. Use the ownership branches in `docs/DEVELOPMENT_WORKFLOW.md`; do not work directly on `main`.

Recommended foundation commit:

```bash
git add .
git commit -m "chore: initialize InsureAssist project foundation"
```