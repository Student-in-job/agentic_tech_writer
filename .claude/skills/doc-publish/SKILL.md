---
name: doc-publish
description: Publish a canonical Markdown document from this workspace to a corporate KB (Confluence, Notion, or Google Docs), routing by the doc's `backend` frontmatter. Markdown stays the source of truth; this delivers a rendered copy. Idempotent via publish-map.yaml. Use only when the operator explicitly asks to publish/deliver a specific document.
---

# doc-publish — deliver a canonical .md to a KB (MD stays the source of truth)

Routes one document to its backend and performs an **idempotent** create-or-update. Markdown
in Git is canonical (`AGENTS.md` → Documentation Format & Publication); the KB page/file is a
rendered output. See [`publish/README.md`](../../../publish/README.md) for the pipeline.

> [!IMPORTANT]
> **Manual and operator-initiated only** (`AGENTS.md` §4). Never on save, in bulk, or
> automatically. Confirm the exact document, backend, and target before publishing, and get
> an explicit "go" before any create/update. Dry-run first.

## Preconditions

- The document lives in `docs/` (not `drafts/`), is review-ready (`status: review` or
  `approved`), and has valid frontmatter with `backend` + `target`.
- The backend's transport is reachable (see matrix below). If not, **stop** and tell the
  operator exactly what is missing — do not improvise another transport.

## Procedure

1. **Read & route** — load the doc's frontmatter. `backend` selects the path; `target` gives
   the destination. `unit: multi` → plan the parent + one child per unit.
2. **Look up the map** — read [`publish/publish-map.yaml`](../../../publish/publish-map.yaml).
   If the doc already has an id for this backend → **update**; else → **create**.
3. **Convert (pure script)** — run the matching converter in
   [`publish/scripts/`](../../../publish/scripts/) to produce the backend payload. These are
   side-effect-free; run them to preview. Rewrite relative links / `[[wikilinks]]` via the map.
4. **Confirm** — show the operator: document, backend, target, create-vs-update, and (dry-run)
   the payload summary. Wait for an explicit "go".
5. **Transport via MCP** — perform the create/update:
   - **Notion** → Notion MCP (`notion-create-pages` / `notion-update-page`).
   - **Google Docs** → Google Docs connector / `google-workspace` skill.
   - **Confluence** → delegate to the [`confluence-publish`](../confluence-publish/SKILL.md)
     skill (REST storage-format transport until an Atlassian MCP is wired).
6. **Record** — write `{backend: {id, url, version, published_at}}` back into
   `publish-map.yaml`, and update the document's changelog/`status` as its template dictates.
7. **Report** — give the operator the link(s) to what was created/updated.

## Backend transport matrix

| `backend` | Transport | Status |
|-----------|-----------|--------|
| `notion` | Notion MCP | active |
| `gdocs` | Google Docs connector / `google-workspace` | available |
| `confluence` | `confluence-publish` (REST) → Atlassian MCP later | planned (needs base URL + space + token) |
| `md` | already canonical — no external publish | n/a |

## Rules

- **MD → backend only.** Never treat a published page as the source. If a page was edited in
  the KB, reconcile it back into the `.md` first, then re-publish.
- **Idempotent.** Always consult `publish-map.yaml`; never create a duplicate of a doc that
  already has an id. `--new` / deleting the mapping forces a fresh create.
- **No secrets in the repo.** Tokens come from the environment; the map stores only ids/urls.
- Read/write only inside `local_documentation/`.
