# Developer Ownership

Ownership minimizes merge conflicts during four-person parallel development. It is not permission to change contracts independently.

## Developer 1 — Web Frontend

Owns `apps/web/**`.

Future responsibilities:

- Agent-facing dashboard.
- Product selector and question interface.
- AI answer and citation/source presentation.
- Loading, error, and success states.
- Responsive sales-agent UX.

Must not modify `services/api/**` without coordination. Uses only the documented backend API and keeps secrets, AI calls, and product logic out of the browser.

## Developer 2 — Backend / API

Owns core backend areas under `services/api/**`.

Future responsibilities:

- FastAPI endpoints and validation.
- API schemas and consistent errors.
- Document and product services.
- Knowledge retrieval integration.

Must not modify frontend files without coordination and must preserve `docs/API_CONTRACT.md`.

## Developer 3 — AI / Product Knowledge / Automation

Future responsibilities:

- AI integration and prompt engineering.
- Product-knowledge retrieval and document ingestion.
- Answer grounding and citations.
- n8n automation.

Prefer future ownership directories:

- `services/api/app/services/ai/`
- `services/api/app/services/knowledge/`
- `services/api/app/services/automation/`

Developer 2 and Developer 3 must coordinate before changing shared backend code. FastAPI owns product logic; n8n owns only follow-up automation.

## Developer 4 — Integration / Product / Deployment

Responsibilities:

- Git integration and PR review.
- API contract coordination.
- Environment configuration.
- Netlify and backend deployment.
- End-to-end testing.
- Demo preparation and scope management.
- Integration bug fixing.

Developer 4 should not own a large isolated feature. Their primary responsibility is to make the entire demo work reliably and keep `main` runnable.

## Shared governance

Root files, `docs/**`, `.github/**`, API contracts, and cross-area changes require coordination with Developer 4. Developers should avoid editing another ownership area, keep PRs small, and resolve interface changes in documentation before implementation.
