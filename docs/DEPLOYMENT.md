# Backend Deployment

The production API runs on the Ubuntu host at `13.250.105.96`. Nginx terminates HTTPS and proxies to Uvicorn on `127.0.0.1:8000`.

## Automatic deployment

`.github/workflows/deploy-api.yml` runs when `main` changes under `services/api/**` or when the workflow itself changes.

The workflow:

1. Installs the API dependencies in a clean Python 3.12 runner.
2. Runs the backend tests.
3. Packages only `services/api`.
4. Uploads a commit-specific release over SSH.
5. Creates an isolated virtual environment on the server.
6. Atomically switches `/opt/insureassist-api/current`.
7. Restarts `insureassist-api`.
8. Verifies `GET /api/v1/health` and restores the previous release on failure.

Deployments are serialized so two production releases cannot run concurrently.

## GitHub configuration

The `production` GitHub environment uses these Actions secrets:

- `PRODUCTION_HOST`
- `PRODUCTION_USER`
- `PRODUCTION_SSH_KEY`
- `PRODUCTION_KNOWN_HOSTS`

Never commit the SSH private key or copy its value into logs.

## Server layout

```text
/opt/insureassist-api/
├── current -> releases/<git-sha>-<workflow-run>-<attempt>
└── releases/

/etc/insureassist-api.env
/etc/systemd/system/insureassist-api.service
/etc/nginx/sites-available/insureassist-api
```

Runtime secrets and production settings belong in `/etc/insureassist-api.env`, readable only by root. The current foundation uses:

```dotenv
APP_ENV=production
CORS_ORIGINS=http://localhost:3000
```

Replace `CORS_ORIGINS` with the deployed Netlify origin before browser integration.

## HTTPS

The current endpoint uses a short-lived Let's Encrypt IP-address certificate for `13.250.105.96`. These certificates last approximately six days, so Certbot renewal and an Nginx reload hook must remain enabled.

Production health URL:

```text
https://13.250.105.96/api/v1/health
```

## Operational commands

```bash
sudo systemctl status insureassist-api
sudo journalctl -u insureassist-api --since "15 minutes ago"
sudo nginx -t
sudo certbot renew --dry-run
```
