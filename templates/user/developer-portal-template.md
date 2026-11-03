---
template: developer-portal
title: Developer Portal (public API)
standard: none
unit: multi
backends: [confluence, gdocs, md]
category: user
---

---
title: <API Product> — Developer Portal
author: System Architect Agent
owner: <team/role>            # accountable owner (mirrors CODEOWNERS)
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0                # tied to product/API release; folder per major (AGENTS.md)
status: draft                # draft | review | approved | deprecated
type: documentation
applies_to: <api >= x.y>      # API/product version this portal documents
depends_on: []                # the OpenAPI/AsyncAPI contracts it is built on
backend: confluence
target: <space/parent or drive-folder or docs path>
unit: multi
---

# <API Product> — Developer Portal

> Audience: **external developers** — user documentation where the user is a programmer.
> Built **on top of the OpenAPI/AsyncAPI contracts** ([[Integration / API Contract]]), not
> a replacement for them: the contract is the source of truth; the portal makes it usable.

This is a **multi-unit** document: an overview/landing page + child pages below.

## Landing / overview (parent)
What the API lets developers do, base URLs per environment, how to get access/keys,
support & status channels, versioning policy, links to each section below.

## Child documents (unit: multi)
- `quick-start` — from zero to first successful call in minutes (get a key → call →
  see a response).
- `authentication` — auth scheme, obtaining/rotating credentials, scopes, example signed
  request.
- `guides` — one page per common integration scenario (task-oriented, with code samples).
- `api-reference` — the endpoint/operation reference, generated from and linked to the
  OpenAPI/AsyncAPI contract.
- `examples` — runnable request/response samples, SDK/snippet gallery, Postman collection.
- `errors` — error model, status codes, rate limits, and how to handle them.
- `changelog` — developer-facing API changes per version (see [[Release Notes]]).
