# InsureAssist Web Guidelines

## Ownership and boundaries

- `apps/web` owns the browser-facing Next.js application, its styles, and its frontend-specific configuration.
- Keep changes inside `apps/web` unless the task explicitly authorizes another area.
- Do not modify root files, documentation, backend code, or `.cursor` as part of frontend-only work.

## Before changing code

- Read the repository root documentation and applicable root guidance first.
- Then read this file and any more specific guidance in the directory being changed.
- Confirm the requested work belongs to the web application before editing.

## Backend integration

- Use only documented backend API contracts.
- Do not infer endpoints, payloads, authentication behavior, or response shapes.
- Keep the backend base URL configurable through `NEXT_PUBLIC_API_BASE_URL`.

## Browser safety and architecture

- Never place secrets, private credentials, or privileged tokens in browser code or `NEXT_PUBLIC_*` variables.
- Do not call AI providers directly from the browser.
- Do not implement backend or insurance business logic in the frontend.

## Change discipline

- Make the smallest change that satisfies the request.
- Avoid speculative abstractions, mock product behavior, fake data, and unrelated cleanup.
- Add dependencies only when they are necessary and approved by the task.
