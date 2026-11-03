---
template: frd
title: Functional Requirements (FR)
standard: none
unit: single
backends: [confluence, gdocs, md]
category: requirements
---

---
title: <System / Feature> — Functional Requirements
author: System Architect Agent
owner: <team/role>            # accountable owner (mirrors CODEOWNERS)
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0                # doc version; stable FR-IDs; changelog at end; tag on approval
status: draft                # draft | review | approved | deprecated
type: specification
applies_to: <service >= x.y>  # optional
depends_on: []                # optional
backend: confluence
target: <space/parent or drive-folder or docs path>
unit: single
---

# <System / Feature> — Functional Requirements

## 1. Purpose & scope
What this document covers; the feature/system boundary; out of scope.

## 2. Actors & roles
| Actor | Description | Permissions |
|-------|-------------|-------------|

## 3. Business context
Goal, value, and the process this supports. Link related [[ADR]] / analysis notes.

## 4. Use cases
| UC-ID | Name | Actor | Trigger | Main flow (summary) |
|-------|------|-------|---------|---------------------|

## 5. Functional requirements
Each requirement atomic, testable, uniquely identified.

| FR-ID | Requirement | Priority (MoSCoW) | Related UC | Acceptance criteria |
|-------|-------------|-------------------|------------|---------------------|
| FR-001 | The system SHALL … | Must | UC-01 | Given/When/Then … |

## 6. Business rules
| BR-ID | Rule | Applies to |
|-------|------|-----------|

## 7. Data & inputs/outputs
Key inputs, outputs, validations (detail data model in the technical doc / NFR as needed).

## 8. Dependencies & assumptions
External systems, preconditions, assumptions.

## 9. Open questions
- …

## 10. Traceability
Each FR ↔ use case ↔ (later) endpoint/test. Keep the mapping current.
