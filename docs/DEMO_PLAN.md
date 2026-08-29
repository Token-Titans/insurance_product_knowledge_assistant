# Demo Plan

This is a future demo scenario, not implemented functionality.

## Primary scenario

Sales agent asks:

> What hospitalization benefits does Product A provide?

Planned InsureAssist response:

```text
Simple grounded answer
        ↓
Highlights
- benefit
- limitation
- relevant condition
        ↓
Source: Product A Brochure, Hospital Benefits section
```

Success means the answer is understandable, grounded in an approved source, includes relevant limitations or conditions, and visibly cites that source. Product A is a placeholder; the final demo must use only approved provided documents and facts.

## Secondary scenario

If the should-have comparison feature is complete and stable:

> What is the difference between Product A and Product B?

The response should compare only supported source facts and preserve conditions and citations for each product.

## Optional final action

Only if the core flow is stable:

```text
Create customer follow-up
        ↓
n8n
```

This automation is optional and must not contain product-knowledge logic.

## Demo safeguards

- Use no customer PII.
- Pre-verify the exact approved source sections.
- Do not imply authoritative policy interpretation beyond the sources.
- If information is unsupported, demonstrate a safe unavailable-information response.
- Do not demo optional behavior after feature freeze unless it is already reliable.

None of these scenarios authorizes feature implementation during foundation initialization.
