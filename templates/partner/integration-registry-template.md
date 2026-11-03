---
template: integration-registry
title: Partner Integration Registry
standard: none
unit: multi
backends: [confluence, gdocs, md]
category: partner
---

---
title: Partner Integration Registry
author: System Architect Agent
owner: <team/role>            # accountable owner (mirrors CODEOWNERS)
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0                # doc version; changelog at end
status: draft                # draft | review | approved | deprecated
type: documentation
applies_to:                   # n/a — indexes many partners
depends_on: []                # optional
backend: confluence
target: <space/parent or drive-folder or docs path>
unit: multi
---

# Partner Integration Registry

> Single place to answer "who do we integrate with, how, and who owns it". **Multi-unit**:
> an index (parent) + one page per partner (child).

## Index (parent)
| Partner | Our owning service | API version | Status | Key/cert expires | Page |
|---------|--------------------|-------------|--------|------------------|------|
| <Partner> | <service> | vX | active/sunset | YYYY-MM-DD | → child |

## Child documents (unit: multi) — one per partner
Each partner page (`partner-<name>`) contains:

### 1. Contacts
Technical + business contacts, support channel, escalation path.

### 2. Documentation
Link to **their** docs, and our saved [[Partner spec snapshot]] of the version we use.

### 3. API & environments
| Environment | Base URL | Credentials location | Notes |
|-------------|----------|----------------------|-------|
| sandbox / prod | … | <secret store ref, not the value> | … |

API version in use; their versioning/deprecation policy.

### 4. Keys, certificates & SLA
Key/cert identifiers (not values), **expiry dates** + renewal owner; SLA (uptime,
response times, support window).

### 5. Ownership on our side
Which of **our** services owns this integration; link [[Partner integration]] (our
technical integration doc) and the relevant [[ADR]].

### 6. Validity
Contract/key validity window; what happens on expiry.
