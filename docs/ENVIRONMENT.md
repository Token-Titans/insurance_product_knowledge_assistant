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

Current foundation values:

```dotenv
APP_ENV=development
CORS_ORIGINS=http://localhost:3000
```

Potential future server-side values, to be added only with the corresponding approved feature:

```dotenv
OPENAI_API_KEY=
OPENAI_MODEL=
N8N_WEBHOOK_URL=
```

Do not add actual values to documentation or source control. AI and n8n credentials belong only in the backend deployment environment.

## Local addresses

- Web: `http://localhost:3000`
- API: `http://localhost:8000`
- Health: `http://localhost:8000/api/v1/health`

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
