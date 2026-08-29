# n8n Workflow

Status: **PLANNED**. No automation is implemented in the foundation. This document describes agreed intent for the optional follow-up automation described in `docs/PRODUCT_SCOPE.md` and `docs/DEMO_PLAN.md`. It does not authorize implementation.

Build this only after the core journey in `docs/PRODUCT_SCOPE.md` is stable.

## Boundary

n8n executes optional email, reminder, and sales follow-up workflows. It must not contain product-knowledge logic.

n8n must never:

- Retrieve, chunk, index, or search approved product documents.
- Call an LLM or generate answer text.
- Decide whether an answer is grounded.
- Receive requests directly from the browser.
- Hold or return product facts that did not come from the API response.

All product knowledge, retrieval, grounding, and confidence handling stay in FastAPI, per `docs/ARCHITECTURE.md` and `docs/KNOWLEDGE_STRATEGY.md`. n8n receives an already-grounded payload and delivers it.

## Position in the architecture

```text
                  SALES AGENT
                       │
                       ▼
                  Next.js Web
                       │
                     HTTPS
                       │
                       ▼
                    FastAPI
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
        Knowledge +          Automation
        LLM (grounded         request
        answer + sources)         │
                                  ▼
                            n8n webhook
                                  │
                       ┌──────────┴──────────┐
                       ▼                     ▼
                 Follow-up draft      Knowledge gap
                 to agent             escalation
```

The web app calls only documented API endpoints. FastAPI calls n8n. The webhook URL stays server-side, per `docs/SECURITY.md`.

## Demo safety: no customer PII

`docs/DEMO_PLAN.md` requires no customer PII, and `docs/PRODUCT_SCOPE.md` places CRM and lead management out of scope.

Therefore the follow-up workflow sends to **the agent's own address**, producing a draft the agent forwards themselves. Do not collect customer email addresses, names, or policy numbers for the demo. This keeps the automation useful while staying inside scope.

## Workflow 1 — Follow-up draft for the agent

The demo workflow. The agent asks a product question, receives a grounded answer, then requests a written follow-up they can send to a customer.

### Input payload

Sent by FastAPI. Every product fact must originate from the `/api/v1/assistant/ask` response; n8n adds nothing.

```json
{
  "recipient_email": "agent@example.com",
  "agent_name": "Agent name",
  "question": "What hospitalization benefits does Product A provide?",
  "answer": "Grounded answer text produced by the API.",
  "important_points": ["Benefit point", "Limitation point"],
  "conditions": ["Relevant condition or exclusion"],
  "sources": [{ "document": "Product A Brochure", "section": "Hospital Benefits" }],
  "confidence": "grounded"
}
```

### Nodes

| # | Node | Type | Configuration |
| --- | --- | --- | --- |
| 1 | Webhook | `webhook` | `POST`, path `insureassist-followup`, respond using Respond node |
| 2 | Normalize | `set` | Flatten `important_points`, `conditions`, `sources` into text; default missing arrays to empty |
| 3 | Grounded and addressed? | `if` | `recipient_email` not empty **and** `confidence` equals `grounded` |
| 4 | Send Draft | `emailSend` / Gmail / Telegram | Body below |
| 5 | Respond OK | `respondToWebhook` | `{ "ok": true }` |
| 6 | Respond 400 | `respondToWebhook` | False branch, status `400` |

Node 3 matters. An answer that is not grounded must not be turned into customer-facing material. Refusing to send is the correct behavior and is worth showing to judges.

### Email body

```text
Subject: Follow-up: {{ $json.question }}

{{ $json.answer }}

Key points
{{ $json.important_points_text }}

Conditions to mention
{{ $json.conditions_text }}

Source
{{ $json.sources_text }}

Prepared by InsureAssist for {{ $json.agent_name }}. Review before sending to a
customer. Confirm against the approved product document; this is not an
authoritative policy interpretation.
```

The closing line is required by `docs/SECURITY.md`, which forbids presenting AI explanations as authoritative interpretation.

### Reminder variant

`docs/PRODUCT_SCOPE.md` also lists reminders. Same workflow with a `wait` node inserted before the send, resuming on a time interval. Keep the delay short for a live demo. Only add this if Workflow 1 already works.

## Workflow 2 — Knowledge gap escalation

Optional, and the stronger differentiator if time allows.

`docs/KNOWLEDGE_STRATEGY.md` requires unsupported information to be acknowledged and the needed source identified. When FastAPI returns a non-grounded confidence, n8n routes the gap to whoever maintains the approved corpus.

```text
Webhook (POST /insureassist-knowledge-gap)
  → Set (normalize)
  → Email or Telegram to the product-knowledge owner
  → Respond to Webhook
```

Input payload:

```json
{
  "question": "Question the corpus could not answer.",
  "confidence": "unsupported",
  "requested_source": "Document or section needed to answer this",
  "agent_name": "Agent name"
}
```

This closes the loop: the assistant admits what it does not know, and the gap becomes a tracked action instead of a dead end. It contains no product-knowledge logic, so it stays within the boundary.

## Required contract and configuration changes

Both workflows need a backend endpoint that does not exist yet. `docs/API_CONTRACT.md` states that a planned example does not authorize implementation, so follow the governance steps before writing code.

Proposed endpoint, subject to approval:

```text
POST /api/v1/assistant/follow-up
```

Governance sequence from `docs/API_CONTRACT.md`:

1. Discuss with the Integration Lead.
2. Add the endpoint and its request and response schema to `docs/API_CONTRACT.md`.
3. Implement the backend.
4. Update the frontend.
5. Test integration.
6. Commit clearly.

Errors use the standard shape:

```json
{
  "detail": { "code": "AUTOMATION_UNAVAILABLE", "message": "Follow-up service is not configured." }
}
```

Configuration, added to `services/api/.env.example` only with the approved feature, per `docs/ENVIRONMENT.md`:

```dotenv
N8N_WEBHOOK_URL=
N8N_KNOWLEDGE_GAP_WEBHOOK_URL=
```

`services/api/app/core/config.py` uses `pydantic-settings` with `extra="ignore"`, so add matching snake_case fields with empty defaults. An unset value must disable the feature cleanly rather than raise on startup.

Never expose these through `NEXT_PUBLIC_*` or `EXPO_PUBLIC_*`.

## Backend integration

```python
async def send_follow_up(payload: dict) -> bool:
    """Forward a grounded answer to the automation webhook."""
    settings = get_settings()
    if not settings.n8n_webhook_url:
        return False
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(settings.n8n_webhook_url, json=payload)
    return response.status_code < 400
```

Rules:

- Automation failure must never break the answer already on screen. Report that follow-up is unavailable and keep the grounded response visible.
- Send only fields the API produced. Do not let the client supply answer text, sources, or confidence, or the grounding guarantee is lost.
- Log outcomes without source text or credentials, per `docs/SECURITY.md`.

## Testing

Use the editor Test URL while building, the Production URL after activating.

```powershell
$body = @{
  recipient_email  = "you@example.com"
  agent_name       = "Test Agent"
  question         = "What hospitalization benefits does Product A provide?"
  answer           = "Placeholder grounded answer."
  important_points = @("Placeholder point")
  conditions       = @("Placeholder condition")
  sources          = @(@{ document = "Product A Brochure"; section = "Hospital Benefits" })
  confidence       = "grounded"
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Uri "https://YOUR-N8N-HOST/webhook/insureassist-followup" `
  -Method Post -ContentType "application/json" -Body $body
```

Also test the refusal path by setting `confidence` to `unsupported` and confirming no email is sent and the response is `400`.

Product A is a placeholder from `docs/DEMO_PLAN.md`. Use only approved documents and facts in the real demo.

## Demo sequence

Runs after the primary scenario in `docs/DEMO_PLAN.md`.

1. Agent asks the hospitalization-benefit question.
2. Grounded answer appears with conditions and a cited source.
3. Agent clicks the follow-up action.
4. A written draft arrives in the agent's inbox or chat, carrying the same source citation.
5. Optional: ask an unsupported question, show the safe unavailable response, and show the gap being escalated instead of answered.

Closing line: the assistant grounds every answer in approved documents, and the automation turns that answer into the agent's next action.

Per `docs/DEMO_PLAN.md`, do not demo optional behavior after feature freeze unless it is already reliable.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `404` from webhook | Workflow inactive, or test URL used in production | Activate, then use the production URL |
| Request hangs | Respond node not reached on one branch | Ensure both IF branches terminate in a Respond node |
| Empty fields in Set node | Payload nested under `body` | Read `$json.body?.field` with a fallback to `$json.field` |
| Arrays render as `[object Object]` | Array passed directly into text | Map to strings in the Set node before use |
| Nothing sent, `400` returned | `confidence` is not `grounded` | Correct behavior, not a bug |
| Email never arrives | SMTP credentials or spam filtering | Prefer Telegram for stage reliability |
| CORS error | Webhook called from the browser | Route through FastAPI |
| Startup failure after adding config | Required setting with no default | Default to empty and disable the feature |

## Build priority

```text
LEVEL 1 — must work
  Ask a product question, receive a grounded answer with conditions and a source

LEVEL 2 — should work
  Workflow 1 follow-up draft, triggered from the UI, refusing non-grounded answers

LEVEL 3 — optional
  Workflow 2 knowledge gap escalation

LEVEL 4 — only with time remaining
  Reminder delay variant, Telegram in addition to email
```

If Level 1 is unreliable at the integration checkpoint in `docs/HACKATHON_RUNBOOK.md`, stop automation work and repair the core journey. Automation without a grounded answer demonstrates nothing.

## Importable definitions

| File | Workflow | Webhook path |
| --- | --- | --- |
| `docs/n8n/insureassist-followup.workflow.json` | Workflow 1 | `insureassist-followup` |
| `docs/n8n/insureassist-knowledge-gap.workflow.json` | Workflow 2 | `insureassist-knowledge-gap` |

Import with **Workflows → ⋯ → Import from File**. Each file carries no credentials, so after import:

1. Open the send node and attach SMTP credentials, or replace it with Gmail or Telegram keeping the same connections.
2. Set a real `fromEmail`, and in Workflow 2 a real knowledge-owner address.
3. Activate the workflow, then copy the production webhook URL into the backend environment.

Both files are placeholder-safe: they contain no product facts, no real addresses, and no credentials.
