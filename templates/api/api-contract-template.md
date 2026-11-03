---
template: api-contract
title: Integration / API Contract
standard: none
unit: single
backends: [confluence, gdocs, md]
category: api
---

---
title: <Service> — Integration / API Contract
author: System Architect Agent
owner: <team/role>            # accountable owner (mirrors CODEOWNERS)
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0                # SemVer: MAJOR breaking · MINOR new fields/endpoints · PATCH docs
status: draft                # draft | review | approved | deprecated
type: specification
applies_to: <service >= x.y>  # the service this contract belongs to
depends_on: []                # optional
backend: confluence
target: <space/parent or drive-folder or docs path>
unit: single
# CI: check backward-compat with oasdiff (OpenAPI) / buf breaking (proto).
---

# <Service> — Integration / API Contract

## 1. Overview
What this API/integration does, who consumes it, protocol (REST/gRPC/messaging), base URL.

## 2. Boundaries & style
Sync/async, versioning scheme, pagination, idempotency, rate limits.

## 3. AuthN / AuthZ
Scheme (OAuth2/JWT/API key), scopes/roles, token lifetime, error on auth failure.

## 4. Endpoints / operations
| Method | Path / Topic | Auth | Description |
|--------|--------------|------|-------------|
| GET | /… | … | … |

### <Method Path> — details
- **Request:** params / headers / body schema.
- **Response:** status codes + body schema.
- **Errors:** error model, codes, ret/idempotency semantics.

```json
// request / response example
```

## 5. Data schemas
| Schema | Field | Type | Required | Notes |
|--------|-------|------|----------|-------|

## 6. Async contracts (if any)
Channels/topics, message schema, delivery guarantees, ordering, DLQ.

## 7. Failure & resilience
Timeouts, retries, circuit-breaking, backward/forward compatibility rules.

## 8. Changelog & compatibility
Versioned changes and any breaking-change policy.
