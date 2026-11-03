---
template: glossary
title: Domain Glossary
standard: none
unit: single
backends: [confluence, gdocs, md]
category: requirements
---

---
title: <Domain / System> — Glossary
author: System Architect Agent
owner: <team/role>            # accountable owner (mirrors CODEOWNERS)
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0                # doc version; changelog at end
status: draft                # draft | review | approved | deprecated
type: documentation
applies_to: <service >= x.y>  # optional
depends_on: []                # optional
backend: confluence
target: <space/parent or drive-folder or docs path>
unit: single
---

# <Domain / System> — Glossary

Shared vocabulary for the domain.

> [!IMPORTANT]
> In a microservice landscape the **same word often means different things in different
> services**. When a term is overloaded, record the meaning **per bounded context** in the
> "Context / owning service" column — do not collapse them into one definition.

## 1. Terms
| Term | Definition | Context / owning service | Synonyms / do-not-confuse-with |
|------|------------|--------------------------|--------------------------------|
| <Term> | <precise, one-sentence meaning> | <service / bounded context> | <aliases; terms it is confused with> |

## 2. Abbreviations & acronyms
| Short | Expansion | Notes |
|-------|-----------|-------|

## 3. Overloaded terms (same word, different meaning)
| Term | Service A means… | Service B means… |
|------|------------------|------------------|

## 4. References
Source systems, [[Functional Requirements]], domain models, [[Data model]].
