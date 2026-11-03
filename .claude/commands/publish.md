---
description: Publish a canonical .md to a KB — Confluence, Notion, or Google Docs (manual, operator-initiated)
argument-hint: <document in docs/> [backend: confluence|notion|gdocs]
---

Use the **doc-publish** skill to publish: `$ARGUMENTS`

Canonical Markdown is the source of truth; this delivers a rendered copy (AGENTS.md →
Documentation Format & Publication). This is a manual, operator-initiated delivery
(AGENTS.md §4 — No Auto-Publish).

Before publishing, route by the doc's `backend` frontmatter (or the one I pass), consult
`publish/publish-map.yaml` for create-vs-update, **dry-run the conversion**, and confirm with
me: the exact document, backend, target space/folder/parent, and create-new vs update-existing.
Publish only on my explicit "go", then record the returned id/url back into the map and report
the link. If the chosen backend's transport is not reachable, stop and tell me what is needed
instead of using another transport.
