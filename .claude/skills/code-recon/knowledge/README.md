# code-recon knowledge base

One file per language/framework. `code-recon` detects the stack, then loads **only** the
matching KB here (progressive disclosure). This keeps the skill small and lets the role
grow to new stacks without rewriting `code-recon`.

## Files

- [`_TEMPLATE.md`](_TEMPLATE.md) — canonical KB structure. Copy it for any new framework.
- `laravel.md`, `quarkus.md`, `spring.md`, `fastapi.md`, `vue.md` — current KBs.

## How to add a KB for a new framework

Do it by hand, or run the **[`kb-author`](../../kb-author/SKILL.md)** skill which automates
these steps:

1. **Copy** `_TEMPLATE.md` → `<stack>.md` (lowercase, short slug, e.g. `django.md`).
2. **Research** the framework's real conventions — README-first for the ecosystem, then
   verify current syntax/version via the **context7 MCP** (resolve the library, query
   "routing", "authentication", "background tasks"). Do not write from memory alone.
3. **Fill every section**, keeping the order. Each entry-point kind MUST have concrete
   **Grep markers** (real annotations/decorators/function names), not vague prose.
4. **Note version differences** where conventions changed across major versions.
5. **Register the stack** in two places so detection works:
   - `code-recon/SKILL.md` → *Step 1* (manifest → stack mapping) and *Step 2* (KB table).
   - `AGENTS.md` → *Workspace Configuration* → supported code stacks.
6. **Sanity-check** the markers against a real repo of that stack if one is available.

## Conventions

- File name = the stack slug used in template frontmatter `stack:` and the SKILL.md tables.
- Keep KBs focused on **what `code-recon` needs**: entry points, auth, data access,
  integrations, gotchas — not a general framework tutorial.
- `_TEMPLATE.md` is not a stack; it is skipped by detection (leading underscore).
