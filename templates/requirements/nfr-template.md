---
template: nfr
title: Non-Functional Requirements (NFR)
standard: none
unit: single
backends: [confluence, gdocs, md]
category: requirements
---

---
title: <System / Feature> — Non-Functional Requirements
author: System Architect Agent
owner: <team/role>            # accountable owner (mirrors CODEOWNERS)
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0                # doc version; stable NFR-IDs; changelog at end; tag on approval
status: draft                # draft | review | approved | deprecated
type: specification
applies_to: <service >= x.y>  # optional
depends_on: []                # optional
backend: confluence
target: <space/parent or drive-folder or docs path>
unit: single
---

# <System / Feature> — Non-Functional Requirements

Quality attributes organized per **ISO/IEC 25010**. Each NFR must be **measurable**
(metric + target), not a wish. Mark `N/A — <reason>` where a category does not apply.

| NFR-ID | Category | Requirement | Metric | Target | Verification |
|--------|----------|-------------|--------|--------|--------------|
| NFR-001 | Performance efficiency | … | p95 latency | ≤ 300 ms | load test |

## 1. Performance efficiency
Throughput, latency, resource usage, capacity/limits.

## 2. Reliability & availability
Availability SLO, RTO/RPO, fault tolerance, retries, degradation modes.

## 3. Security
AuthN/AuthZ, data protection (in transit/at rest), audit, compliance (list standards).

## 4. Scalability
Horizontal/vertical scaling, expected growth, back-pressure.

## 5. Maintainability
Modularity, testability, observability (logs/metrics/traces), deployment cadence.

## 6. Usability & accessibility
UX expectations, accessibility standard (e.g. WCAG level), i18n/l10n.

## 7. Compatibility & portability
Supported platforms/browsers, integrations, migration/rollback.

## 8. Constraints
Regulatory, budget, technology, operational constraints that bound the design.

## 9. Traceability
Each NFR ↔ affected components/endpoints ↔ verification method.
