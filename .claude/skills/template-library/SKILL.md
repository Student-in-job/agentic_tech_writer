---
name: template-library
description: Ask which document template to use, apply it, and maintain the template library. Handles the storage-aware "document unit" — a Confluence page, a Google Docs file, or a Markdown file — and single vs multi-unit documents (e.g. an API library split by module/service/microservice). Use when starting a document, choosing a template, or adding/updating a template in the library.
---

# template-library — choose, apply, and maintain document templates

The analyst+tech-writer role writes many kinds of documents. This skill is the front door:
it **asks which template** fits, **applies** it, and **maintains** the library. It also
resolves the abstract **document unit** to the target storage backend.

## Core concept — the "document unit"

A *document* is one logical unit. How it materializes depends on the storage backend:

| Backend | A document is… | Multi-unit document (split) |
|---------|----------------|------------------------------|
| **Confluence** | a **page** (in a space, under a parent) | a **parent page + child pages** |
| **Google Docs** | a **file** (in a Drive folder) | a **folder + files** |
| **Markdown** | an **`.md` file** (in `docs/` / `drafts/`) | a **folder + `.md` files** |

- **single** — one page/file (most doc types: ADR, runbook, release notes…).
- **multi** — a tree: one parent/overview + one child per part. Used for the
  **API library split by module / service / microservice** and large technical docs.

Templates are written **backend-agnostic** (plain Markdown sections). The mapping to
page/file happens at author time here and at publish time in the publish skills
(`confluence-publish` for Confluence).

## The library

Catalog: [`../../../templates/README.md`](../../../templates/README.md) — the list of
templates (id, title, standard, unit, backends, path). Templates live under
`templates/<category>/`. Meta-template for authoring new ones:
[`../../../templates/_meta-template.md`](../../../templates/_meta-template.md).

Each template file declares its contract in frontmatter:
`template`, `title`, `standard` (none | C4 | TOGAF | BIAN), `unit` (single | multi),
`backends`.

## Procedures

### A. Start a document (ask & apply)
1. **Ask the operator** (or infer from the request): what kind of document, and the
   **storage backend** (Confluence / Google Docs / Markdown; default backend =
   Confluence per `AGENTS.md`).
2. Look up the catalog. If several fit, list them and ask which.
3. Resolve the **unit**: single → one page/file; multi → confirm the split axis
   (module / service / microservice) and plan the parent + children.
4. Copy the template into `drafts/` (`.md` working copy), fill frontmatter
   (`backend`, `unit`, target space/folder). Hand technical sections to `code-recon`
   and diagrams to `diagram-builder` as needed.
5. Draft only — never publish. Delivery is a separate operator-initiated step.

### B. Maintain the library (add / update a template)
1. Confirm the template **id**, **title**, **standard**, **unit**, and **backends**.
2. Copy [`_meta-template.md`](../../../templates/_meta-template.md) into the right
   `templates/<category>/<id>-template.md` and fill it.
3. For a **standard-based** template (C4 / TOGAF / BIAN), **ground it** — verify the
   standard's real artifacts/sections via web or the **context7 MCP** before writing;
   do not invent structure from memory.
4. **Register** it: add a row to `templates/README.md` catalog.
5. Keep templates focused and consistent with the meta-template's section contract.

## Rules

- Read/write only inside `local_documentation/`. Draft in `drafts/`.
- **No auto-publish** (`AGENTS.md` §4). Choosing a backend here does not publish — it
  only decides how the unit will be rendered later.
- Relative markdown links; new docs carry the standard frontmatter.
