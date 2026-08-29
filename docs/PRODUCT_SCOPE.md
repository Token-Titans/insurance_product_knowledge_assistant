# Product Scope

This document is the binding product boundary for InsureAssist.

## Challenge

**Reimagining Customer Engagement Through AI-Powered Digital Assistants**

## User

**Insurance Sales Agent**

## Problem

Agents need fast and consistent access to insurance product information when preparing for or speaking with customers. Today, benefits, eligibility, exclusions, coverage conditions, and product differences may be spread across brochures, policy documents, benefit tables, guides, FAQs, and training material.

## MVP

The agent can ask a natural-language question about supported insurance products and receive a clear grounded answer with important conditions and source information.

## Core journey

```text
Agent opens InsureAssist
        ↓
Selects product / asks question
        ↓
AI retrieves approved product information
        ↓
Answer displayed
        ↓
Important conditions/exclusions highlighted
        ↓
Source reference displayed
```

Optional final step: create a follow-up action via n8n.

## Must have — future

- Ask a product question.
- Retrieve relevant approved knowledge.
- Generate an understandable answer.
- Identify important conditions and exclusions.
- Show a source/reference.
- Handle unavailable information safely.

## Should have

- Product comparison.
- Suggested sales questions.
- Simple customer-friendly explanation.
- Follow-up automation.

## Nice to have

- Voice.
- Multilingual answers.
- Conversation history.
- Recommended talking points.

## Out of scope

- Customer-facing chatbot.
- Claims.
- Underwriting.
- Quotation or premium calculation.
- Policy issuance.
- Payment.
- CRM or lead management.
- Authentication.
- Full document management.
- Enterprise search platform.
- Autonomous sales agent.

## Foundation rule

The current initialization must not implement AI calls, OpenAI SDKs, RAG, embeddings, vector databases, document upload, PDF extraction, question answering, product comparison, n8n workflows, customer follow-up, authentication, databases, chatbot interfaces, product UI, or fake product data. Only the API health endpoint is implemented. Do not expand scope unless explicitly requested later.
