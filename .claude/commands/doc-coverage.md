---
description: Assess documentation completeness for a service/project and decide gaps
argument-hint: "<service|project name> (e.g. mfo-service) — empty = all"
---

Use the **doc-coverage** skill for: `$ARGUMENTS`

Compute documentation coverage (expected set from `templates/coverage-profile.yaml` filtered by
the target's facets in `docs/registry.yaml`, vs. actual docs in `docs/` + `drafts/`), save the
report to the target's `coverage.md`, then discuss the gaps with the operator — per missing doc:
**create now** (→ `doc-new`), **defer**, or **mark N/A** (record a waiver in the registry).
Never auto-create; operator-gated.
