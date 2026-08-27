---
description: Add a code-recon knowledge-base for a new language/framework (kb-author)
argument-hint: <framework> [version]
---

Use the **kb-author** skill to add a knowledge-base for: `$ARGUMENTS`

Follow the skill: confirm language/framework/version and a slug → research the real
conventions (README-first, then verify current syntax via context7 MCP — do not write from
memory) → copy `_TEMPLATE.md` to `knowledge/<slug>.md` and fill every section with concrete
Grep markers → register the stack in `code-recon/SKILL.md` (Step 1 + Step 2) and in
`AGENTS.md` Workspace Configuration → validate markers against a real repo if available.
