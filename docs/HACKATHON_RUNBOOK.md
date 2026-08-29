# Four-Hour Hackathon Runbook

## Timeline

- **00:00–00:20 — Foundation + final scope:** confirm runnable scaffolds, ownership, contract, approved document set, and branch readiness.
- **00:20–01:40 — Parallel feature development:** developers work in their ownership branches against the agreed contract.
- **01:40–02:00 — First integration:** combine the minimum vertical flow and resolve contract mismatches.
- **02:00 — END-TO-END MVP MUST WORK.**
- **02:00–02:45 — Improve answer quality + UX:** strengthen grounding, conditions, sources, and scanability only after the core flow works.
- **02:45–03:15 — Deployment / integration / fixes:** deploy, verify environments, and fix end-to-end failures.
- **03:15 — FEATURE FREEZE.**
- **03:15–03:40 — Demo polish:** stabilize approved scenarios, errors, and presentation.
- **03:40–04:00 — Demo rehearsal:** run the full script and prepare fallback evidence.

## Critical rule

If this flow does not work by Hour 2:

```text
Question → knowledge retrieval → grounded AI answer → source
```

stop all optional development and focus the entire team on making it reliable.

## Operating rules

- Developer 4 integrates early and keeps `main` runnable.
- API changes are coordinated and documented before both sides change.
- Use only approved documents and non-PII demo questions.
- Fix broken core behavior before UX polish.
- After feature freeze, accept only demo-critical fixes.
- Do not add comparison, automation, voice, multilingual support, history, or talking points unless the must-have flow is stable.

## Foundation exit check

- Web lint and build pass.
- API tests pass.
- Health endpoint returns the documented response.
- No secrets or product features were added.
- Scope, contract, knowledge strategy, ownership, and branch workflow are clear.
- Four developers can begin on their assigned branches immediately.
