---
template: legal-register
title: Legal & Contractual Register (pointers)
standard: none
unit: single
backends: [confluence, gdocs, md]
category: partner
---

---
title: <Partner / Scope> — Legal & Contractual Register
author: System Architect Agent
owner: <team/role>            # accountable owner (mirrors CODEOWNERS)
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0                # register version (pointers only — no contract content)
status: draft                # draft | review | approved | deprecated
type: documentation
applies_to:                   # n/a
depends_on: []                # optional
backend: confluence
target: <restricted space/folder — access-controlled>
unit: single
---

# <Partner / Scope> — Legal & Contractual Register

> [!WARNING]
> Contracts, NDAs and signed SLAs are **business documents that live in a separate,
> access-restricted store**. This register holds only **pointers and metadata** — never
> paste contract text, signatures, or confidential terms here. Link to the controlled
> store instead.

## Register
| Document | Type | Counterparty | Store location (link) | Access owner | Effective | Expires / renews | Linked integration |
|----------|------|--------------|-----------------------|--------------|-----------|------------------|--------------------|
| <name> | Contract / NDA / SLA | … | <restricted store ref> | … | YYYY-MM-DD | YYYY-MM-DD | [[Partner integration registry]] |

## Key obligations (non-confidential summary)
Only non-confidential, operationally relevant points (e.g. SLA targets, notice periods)
that engineering/ops need. Anything sensitive stays in the restricted store.

## Renewals & alerts
Upcoming expiries and who is responsible for renewal.
