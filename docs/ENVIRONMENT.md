# Environment

Commit only `.env.example` files. Create local `.env` files as needed and never commit credentials.

## Web

Location: `client/.env.example`

```dotenv
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

`NEXT_PUBLIC_*` values are visible in the browser and must never contain secrets.

Vercel production and preview environments use:

```dotenv
NEXT_PUBLIC_API_BASE_URL=https://13.250.105.96
```

Production web URL: `https://insureassist-cyan.vercel.app`

## API

Location: `services/api/.env.example`

```dotenv
APP_ENV=development
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
N8N_WEBHOOK_URL=
```

`OPENAI_API_KEY` is server-side only. Leave it empty for extractive answers from approved documents. Set it locally in `.env` (never commit the file) to enable ChatGPT/OpenAI generation.

`N8N_WEBHOOK_URL` is server-side only. Leave it empty to disable follow-up. Use the n8n test URL while the editor is listening, and the production URL after the workflow is Active.

Do not add actual values to documentation or source control. AI and n8n credentials belong only in the backend deployment environment.

## Local addresses

- Web: `http://localhost:3000`
- API: `http://localhost:8000`
- Health: `http://localhost:8000/health`
- Products: `http://localhost:8000/products`
- Suggested questions: `http://localhost:8000/products/{id}/suggested-questions`
- Ask: `POST http://localhost:8000/assistant/ask`
- Compare: `POST http://localhost:8000/assistant/compare`
- Follow-up: `POST http://localhost:8000/assistant/follow-up`
- Swagger: `http://localhost:8000/docs`
- Compatibility prefix: `/api/v1` (same handlers)

## Production API

- Base URL: `https://13.250.105.96`
- Health: `https://13.250.105.96/api/v1/health`
- Runtime environment file: `/etc/insureassist-api.env` on the production host

GitHub Actions deployment configuration is documented in `docs/DEPLOYMENT.md`. Production secrets must stay in GitHub Actions secrets or the root-owned server environment file.

Production CORS includes `https://insureassist-cyan.vercel.app` and the local development origin.

## Validation

```bash
# client
npm install
npm run lint
npm run build

# services/api
pip install -r requirements.txt
pytest
```

Deployment targets are Vercel for the web app, the documented Ubuntu host for FastAPI, and n8n Cloud or a hackathon environment for any future automation.
