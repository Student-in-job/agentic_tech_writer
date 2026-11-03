---
template: vision
title: Vision / One-pager
standard: none
unit: single
backends: [confluence, gdocs, md]
category: requirements
---

---
title: <Product / Initiative> — Vision
author: System Architect Agent
owner: <team/role>            # accountable owner (mirrors CODEOWNERS)
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0                # doc version; changelog at end; tag repo on approval (AGENTS.md)
status: draft                # draft | review | approved | deprecated
type: specification
applies_to: <service >= x.y>  # optional — the code/version this describes
depends_on: []                # optional, e.g. [payment-api@2.x]
backend: confluence
target: <space/parent or drive-folder or docs path>
unit: single
---

# <Product / Initiative> — Vision

> One page that answers **"why"**. If it does not fit on a page, it is not a vision — it is a spec.

## 1. Problem
The problem being solved, for whom, and why it matters now.

## 2. Target users
| Segment | Who they are | What they need |
|---------|--------------|----------------|

## 3. Goals & success metrics
| Goal | Metric | Baseline | Target |
|------|--------|----------|--------|

## 4. Scope
- **In scope:** what this initiative delivers.
- **Out of scope:** explicitly what it does **not** cover (prevents scope creep).

## 5. Approach (1 paragraph)
The high-level idea of how we solve it. Link the deeper docs: [[Functional Requirements]],
[[C4 architecture]], [[ADR]].

## 6. Risks & assumptions
| Item | Risk / assumption | Impact |
|------|-------------------|--------|
