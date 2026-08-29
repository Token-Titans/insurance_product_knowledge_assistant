# Frontend: follow-up reminder (n8n)

This guide is for Developer 1 (`client/`). The backend endpoint is already implemented. Wire **Create follow-up** to FastAPI only. The browser must never call n8n.

Authority: `docs/API_CONTRACT.md`. Do not invent extra fields.

## What the user sees

```text
Sales agent asks a product question
        ↓
InsureAssist shows a grounded answer
        ↓
Agent clicks Create follow-up
        ↓
Agent fills customer name, date, and note
        ↓
Web app POSTs /assistant/follow-up
        ↓
FastAPI posts to n8n
        ↓
n8n waits until follow_up_date, then emails the agent
```

n8n Wait and SMTP are not frontend work. After `status: "scheduled"`, show success and close the dialog.

## Do not do this

- Do not `fetch` `https://avinn.app.n8n.cloud/webhook/...` from the client.
- Do not put `N8N_WEBHOOK_URL` in `NEXT_PUBLIC_*`.
- Do not send answer text, sources, or confidence. FastAPI already has the product catalog; n8n only needs the reminder fields.
- Do not collect customer email, phone, or policy number. `customer_name` is a demo label for the reminder (first name is enough).

## When to show the button

`FollowUpButton` already sits in `client/features/assistant/components/answer-panel.tsx`, which only renders for `turn.status === "answered"`.

Pass the current turn’s `productId` into the button. That id is on `ChatTurn.productId` in `client/features/assistant/types/ask-screen.types.ts`.

Hide or disable follow-up on `unavailable` and `error` turns.

## Endpoint

```text
POST {NEXT_PUBLIC_API_BASE_URL}/assistant/follow-up
Content-Type: application/json
```

Use the existing Axios instance in `client/shared/lib/api.ts` (same as ask). Local default is often `http://localhost:8000`. Production uses `NEXT_PUBLIC_API_BASE_URL` (currently the FastAPI host, including `/api/v1` if that is how the app is configured).

The same handler exists at `/api/v1/assistant/follow-up`.

### Request

```json
{
  "customer_name": "Aung Aung",
  "product_id": "dai-ichi-life-pro",
  "follow_up_date": "2026-09-05",
  "note": "Call back about the Life Pro living benefit."
}
```

| Field | Source in UI | Rules |
| --- | --- | --- |
| `customer_name` | Text input | Required, 1–120 characters |
| `product_id` | Selected product on that chat turn | Required. Do not let the agent re-type it. Send `turn.productId` |
| `follow_up_date` | Date input | `YYYY-MM-DD`. Must be **today or later** |
| `note` | Textarea | Required, 1–2000 characters |

`product` (display name) is filled by the API. Do not send it.

### Success (HTTP 200)

```json
{
  "status": "scheduled",
  "customer_name": "Aung Aung",
  "product": "Dai-ichi Life Pro",
  "follow_up_date": "2026-09-05"
}
```

Show a short confirmation using `product` and `follow_up_date`. Then close the dialog.

### Errors

Same shape as the rest of the API:

```json
{
  "detail": {
    "code": "ERROR_CODE",
    "message": "Human-readable message"
  }
}
```

Map `detail.code` with `isApiError` from `client/shared/types/api-error.ts`. Do not show raw backend `message` strings in the UI.

| HTTP | `code` | Meaning | UI |
| --- | --- | --- | --- |
| 400 / 422 | `INVALID_REQUEST` | Empty fields, bad date, past date | Keep the dialog open; highlight the field |
| 404 | `PRODUCT_NOT_FOUND` | `product_id` is not in the corpus | Ask them to pick the product again |
| 400 | `FOLLOW_UP_REFUSED` | n8n rejected the payload | Follow-up could not be scheduled |
| 503 | `AUTOMATION_UNAVAILABLE` | `N8N_WEBHOOK_URL` empty or n8n down | Follow-up is not available right now |
| other | `HTTP_ERROR` / generic | Network or server | Try again shortly |

Do not retry 4xx. One retry on 5xx is enough, matching ask.

## Suggested files

Keep the `"use client"` boundary on the dialog, not on the page.

| File | Role |
| --- | --- |
| `client/features/assistant/schemas/follow-up.schema.ts` | Zod: `customer_name`, `product_id`, `follow_up_date`, `note` |
| `client/features/assistant/types/follow-up.types.ts` | `z.infer` types |
| `client/features/assistant/services/follow-up.service.ts` or `client/shared/services/follow-up.service.ts` | `api.post("/assistant/follow-up", body)` then parse |
| `client/features/assistant/queries/follow-up.query.ts` | `useMutation` (schedule is a write, not a query cache) |
| `client/features/assistant/components/follow-up-button.tsx` | Dialog + form |

`FollowUpButton` props:

```ts
interface FollowUpButtonProps {
  productId: string;
}
```

From `answer-panel.tsx` / `chat-turn.tsx`, pass `turn.productId`.

Form: `react-hook-form` + `zodResolver` (four fields). Inputs: shadcn `Input`, `Label`, `Textarea`, existing `Dialog`. Date: `<Input type="date" />` with `min` set to today (`YYYY-MM-DD`). Styling: semantic tokens only (`bg-card`, `text-foreground`, `border-input`, `bg-destructive`).

## i18n

Add every new key to **both** `client/locales/en/assistant.json` and `client/locales/my/assistant.json`. Do not hardcode English in JSX.

Suggested keys (replace the current stub copy):

```text
answered.follow_up
answered.follow_up_title
answered.follow_up_body
answered.follow_up_customer_name
answered.follow_up_date
answered.follow_up_note
answered.follow_up_submit
answered.follow_up_pending
answered.follow_up_success
answered.follow_up_close
ask.errors.AUTOMATION_UNAVAILABLE
ask.errors.FOLLOW_UP_REFUSED
```

`follow_up_success` should interpolate product and date, for example:

```ts
t("answered.follow_up_success", {
  product: result.product,
  date: result.follow_up_date,
});
```

Use `Intl` / i18next date formatting for display. Still send `follow_up_date` as `YYYY-MM-DD`.

## Example service

```ts
export async function scheduleFollowUp(
  payload: FollowUpRequest,
  signal?: AbortSignal,
): Promise<FollowUpResponse> {
  const body = followUpRequestSchema.parse(payload);
  const response = await api.post<unknown>("/assistant/follow-up", body, {
    signal,
  });
  return followUpResponseSchema.parse(response.data);
}
```

## Manual check

1. API running; `N8N_WEBHOOK_URL` set on the **API** `.env`, not in Next.js.
2. n8n workflow **Active**, or click **Listen for test event** if using the test webhook.
3. Ask a grounded question, open Create follow-up, submit a future date.
4. Network tab: one `POST /assistant/follow-up` to FastAPI, **not** to `avinn.app.n8n.cloud`.
5. UI shows scheduled; n8n execution has `customer_name`, `product`, `follow_up_date`, `note`.
6. Submit yesterday’s date → 400, dialog stays open.
7. Stop n8n / unset URL → 503, friendly unavailable copy.

## n8n (not frontend)

FastAPI already sends:

```json
{
  "customer_name": "...",
  "product": "Dai-ichi Life Pro",
  "product_id": "dai-ichi-life-pro",
  "follow_up_date": "2026-09-05",
  "note": "..."
}
```

The workflow must **Respond** to the webhook first, then **Wait** until `follow_up_date`, then **Send Email**. If Wait runs before Respond, the API times out and the UI shows `AUTOMATION_UNAVAILABLE`.
