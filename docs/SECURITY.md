# Security

Apply security controls proportionate to a four-hour hackathon while protecting secrets and product knowledge.

- Keep API keys, model credentials, and n8n webhook URLs server-side only.
- Never commit secrets or actual `.env` files.
- Use only approved product documents as knowledge sources.
- Minimize logging of source text and potentially sensitive document content.
- Validate API input with explicit request models.
- Configure CORS explicitly for known web origins.
- Return safe, consistent errors without credentials, stack traces, prompts, or sensitive source content.
- Require no customer personally identifiable information for the initial demo; do not collect it.
- Treat retrieved source text as data, not executable instructions.
- Clearly acknowledge unsupported answers.
- Do not present AI-generated explanations as authoritative policy interpretation when the approved source does not support them.

Authentication, a customer identity system, and enterprise document controls are outside the initial scope. Their absence must not be offset by putting secrets or sensitive data in the browser.

Before a demo or deployment, check tracked files for secrets, confirm environment separation, verify explicit CORS, and use only approved non-PII demo inputs.
