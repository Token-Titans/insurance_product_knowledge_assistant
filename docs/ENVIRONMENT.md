# Environment

Commit only `.env.example` files. Create local `.env` files as needed and never commit credentials.

## Web

Location: `apps/web/.env.example`

```dotenv
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

`NEXT_PUBLIC_*` values are visible in the browser and must never contain secrets.

## API

Location: `services/api/.env.example`

```dotenv
APP_ENV=development
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
```

`OPENAI_API_KEY` is server-side only. Leave it empty for extractive answers from approved documents. Set it locally in `.env` (never commit the file) to enable ChatGPT/OpenAI generation.

Potential future server-side values, to be added only with the corresponding approved feature:

```dotenv
N8N_WEBHOOK_URL=
```

Do not add actual values to documentation or source control. AI and n8n credentials belong only in the backend deployment environment.

## Local addresses

- Web: `http://localhost:3000`
- API: `http://localhost:8000`
- Health: `http://localhost:8000/health`
- Products: `http://localhost:8000/products`
- Ask: `POST http://localhost:8000/assistant/ask`
- Swagger: `http://localhost:8000/docs`
- Compatibility prefix: `/api/v1` (same handlers)

## Validation

```bash
# apps/web
npm install
npm run lint
npm run build

# services/api
pip install -r requirements.txt
pytest
```

Deployment targets are Netlify for the web app, Python-capable hosting for FastAPI, and n8n Cloud or a hackathon environment for any future automation.
