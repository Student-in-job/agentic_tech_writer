---
template: partner-spec-snapshot
title: Partner Spec Snapshot
standard: none
unit: single
backends: [confluence, gdocs, md]
category: partner
---

---
title: <Partner> — Spec Snapshot (<version>)
author: System Architect Agent
owner: <team/role>            # accountable owner (mirrors CODEOWNERS)
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: <partner-spec-version>  # = the PARTNER's spec version; this snapshot is frozen (AGENTS.md)
status: approved             # frozen capture — do not edit; new version → new snapshot
type: documentation
applies_to: <partner-api vX.Y>
depends_on: []                # optional
backend: confluence
target: <space/parent or drive-folder or docs path>
unit: single
---

# <Partner> — Spec Snapshot (<version>, captured YYYY-MM-DD)

> [!IMPORTANT]
> Partners change their documentation **without notice**. This is our frozen copy of the
> exact version we integrate against. Do not edit the captured content — if the partner
> publishes a new version, capture a **new** snapshot and link it from the
> [[Partner integration registry]].

## Capture metadata
| Field | Value |
|-------|-------|
| Partner | … |
| Spec version | … |
| Source URL | … |
| Captured on | YYYY-MM-DD |
| Captured by | … |
| Our integration using it | [[Partner integration]] |

## Captured specification
Paste / attach the partner's spec (OpenAPI, PDF, message schemas, field definitions) as it
was on the capture date. Attach the original file where possible.

## Our notes / deviations
Anything ambiguous, partner-specific quirks, fields we rely on, and differences from their
latest published version.
