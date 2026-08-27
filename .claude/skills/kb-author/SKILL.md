---
name: kb-author
description: Add or update a code-recon knowledge-base for a new programming language or framework, so the analyst can support a new stack. Use when the user wants code-recon to handle a framework it doesn't cover yet (e.g. Django, NestJS, Go/gin, Rails), or to refresh an existing KB for a new framework version.
---

# kb-author — author a new framework knowledge-base

Extend the analyst's reach to a new stack by writing a `code-recon` knowledge-base entry.
This is how the technical-writer role grows **without rewriting `code-recon`**.

## Source of truth

- Template: [`../code-recon/knowledge/_TEMPLATE.md`](../code-recon/knowledge/_TEMPLATE.md)
- Authoring guide: [`../code-recon/knowledge/README.md`](../code-recon/knowledge/README.md)
- Existing KBs to match in style: `laravel.md`, `quarkus.md`, `spring.md`, `fastapi.md`,
  `vue.md` in the same folder.

## Procedure

1. **Confirm the stack** with the operator: language, framework, and the target major
   version. Pick a short lowercase slug (e.g. `django`, `nestjs`, `gin`).
2. **Research — do not write from memory:**
   - README-first: how the ecosystem describes routing/entry points.
   - Verify current syntax via the **context7 MCP**: resolve the library id, then query
     `routing`, `authentication`, `background tasks / messaging`, `scheduling`. Capture
     the real decorators/annotations/function names.
3. **Copy** `_TEMPLATE.md` → `../code-recon/knowledge/<slug>.md` and fill **every** section
   in order. Each entry-point kind must carry concrete **Grep markers** (real symbols).
   Note version-specific differences. Omit truly-N/A subsections explicitly.
4. **Register the stack** (both are required for detection to work):
   - Edit [`../code-recon/SKILL.md`](../code-recon/SKILL.md):
     - *Step 1* — add the manifest→stack rule (which dep in which manifest identifies it).
     - *Step 2* — add a row to the KB table pointing at `knowledge/<slug>.md`.
   - Edit [`AGENTS.md`](../../../AGENTS.md) → *Workspace Configuration* → add to supported
     code stacks.
5. **Update** the KB folder guide list in `../code-recon/knowledge/README.md` if you want
   the file enumerated there.
6. **Validate** (if a repo of that stack is reachable): run the new markers with Grep and
   confirm they find real entry points; tighten any that over/under-match.

## Rules

- Read/write only inside `local_documentation/` (KB files live here). Read-only against
  any repo you sample for validation.
- Keep KBs scoped to what `code-recon` needs (entry points, auth, data, integrations,
  gotchas) — not a general tutorial.
- Never invent markers you have not verified against docs (context7) or real code.
