# Knowledge Strategy

This document governs planned product-knowledge and AI behavior. No RAG or AI behavior is implemented in the foundation.

## Approved hackathon corpus

Assume a very small, explicitly approved document set such as:

- Product A brochure.
- Product A benefit table.
- Product B brochure.
- Product B benefit table.
- Product FAQ.

These are examples of document types, not product facts or bundled demo data.

## Principles

- Answers must come from approved provided documents.
- Product documents are the source of truth.
- The model must not rely on general insurance knowledge when product-specific information is required.
- Answers should reference the relevant document and section where possible.
- Unknown or unsupported information must be explicitly acknowledged.
- Relevant conditions and exclusions must not be omitted.
- Source facts must be distinguishable from generated plain-language explanations.
- AI supports sales agents; it does not make final customer decisions or unsupported policy interpretations.
- Credentials remain server-side, outputs should be structured and validated, and unnecessary model calls should be avoided.

## Planned simple RAG concept

```text
Approved documents
        ↓
Extract text
        ↓
Chunk / index
        ↓
Retrieve relevant content
        ↓
LLM
        ↓
Grounded answer + citation
```

The exact model, extraction method, chunking approach, index, retrieval implementation, and confidence handling will be selected during feature development. Do not add an SDK, vector database, PDF library, ingestion pipeline, or generic autonomous agent during foundation initialization.

Hackathon implementation (see `docs/DECISIONS.md` 008): approved markdown in `services/api/app/knowledge/approved/` is split on `#` / `##` headings; retrieval is keyword overlap (top 3); generation is the OpenAI SDK when `OPENAI_API_KEY` is set, otherwise extractive text from retrieved sections. Citations use `title`, `file`, and `section`.

## Safe answer behavior

If the approved sources do not support an answer, state that the information is unavailable and identify what source is needed. Never fabricate a product benefit, limit, eligibility rule, exclusion, or coverage condition.
