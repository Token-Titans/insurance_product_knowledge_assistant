# Development Workflow

## Branches

- `main` — protected, integrated, and always runnable.
- `feature/web-assistant` — Developer 1.
- `feature/api-assistant` — Developer 2.
- `feature/knowledge-rag` — Developer 3.
- `feature/integration` — Developer 4.

## Before changing code

1. Read root `AGENTS.md`.
2. Read `docs/PRODUCT_SCOPE.md`.
3. Identify the ownership area.
4. Read the nearest nested `AGENTS.md`.
5. Read `docs/API_CONTRACT.md` for web/API changes.
6. Read `docs/KNOWLEDGE_STRATEGY.md` for knowledge/AI changes.
7. Read `docs/ARCHITECTURE.md` for architecture changes.
8. Pull the latest integrated work.

## Working rules

- Do not develop directly on `main`.
- Work only in the assigned branch and ownership area unless coordinated.
- Make small, focused commits and push frequently.
- Open small PRs; use `.github/pull_request_template.md`.
- Never silently change API contracts. Coordinate with Developer 4 and update the contract first.
- Do not refactor unrelated working code.
- Add dependencies only for a clear MVP requirement.
- Integrate early rather than waiting for feature completion.
- Run relevant checks and do not merge failed builds or tests.
- Keep `main` runnable and free of secrets.

## Integration checks

Web:

```bash
cd apps/web
npm install
npm run lint
npm run build
```

API:

```bash
cd services/api
pip install -r requirements.txt
pytest
```

Verify `GET /api/v1/health` and frontend/backend compatibility when an integration PR changes either side. Near feature freeze, prioritize fixes to the end-to-end demo over new functionality.
