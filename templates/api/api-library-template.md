---
template: api-library
title: API Library (per module/service)
standard: none
unit: multi
backends: [confluence, gdocs, md]
category: api
---

<!--
MULTI-UNIT template. Materializes as:
- Confluence: a PARENT page (this index) + one CHILD page per module/service/microservice.
- Google Docs / Markdown: a FOLDER with an index file + one file per unit.
Confirm the split axis (module | service | microservice) before generating children.
Each child uses the `api-contract` template.
-->

---
title: <Domain / Platform> — API Library
author: System Architect Agent
owner: <team/role>            # accountable owner (mirrors CODEOWNERS)
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0                # SemVer per unit (contracts); CI oasdiff / buf breaking
status: draft                # draft | review | approved | deprecated
type: documentation
applies_to: <platform >= x.y>  # optional
depends_on: []                 # optional
backend: confluence
target: <space/parent or drive-folder or docs path>
unit: multi
split_by: service            # module | service | microservice
---

# <Domain / Platform> — API Library

Parent/index for the API documentation, split by **<module | service | microservice>**.

## 1. Landscape
What the platform is; how the units relate. One context diagram of the whole.

```mermaid
C4Context
    title API Landscape — <Domain>
```

## 2. Index of units
| Unit | Type | Owner | Base URL / topic | Doc (child) |
|------|------|-------|------------------|-------------|
| <name> | service | … | … | → child page/file |

## 3. Cross-cutting conventions
Shared auth, versioning, error model, pagination, correlation/trace IDs — stated once here
so each child does not repeat them (child links back to this section).

## 4. Child documents (one per unit)
Each child is generated from the **`api-contract`** template:
- Overview, boundaries, auth (inherit §3 unless overridden)
- Endpoints / operations + schemas
- Async contracts, failure/resilience, changelog

> Keep this index in sync when units are added/removed.
