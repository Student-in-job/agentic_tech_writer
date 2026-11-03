---
name: confluence-publish
description: Publish a finished, reviewed document from this workspace to Confluence, respecting Confluence's formatting conventions. The Confluence executor used by the doc-publish router. Use only when the operator explicitly asks to publish/deliver a specific document to Confluence.
---

# confluence-publish — deliver a document to Confluence

> [!IMPORTANT]
> Publishing is **manual and operator-initiated**, per `AGENTS.md` Operating Principles §4
> (Staging Area — No Auto-Publish). Never run this automatically, in bulk, or on save.
> Confirm the exact document, target space, and parent page before publishing.

This is the **Confluence transport** for the [`doc-publish`](../doc-publish/SKILL.md) router
(`backend: confluence`). Markdown stays the source of truth; idempotency via
`publish/publish-map.yaml`. Use the converter `publish/scripts/md_to_confluence.py`.

## Preconditions

- The document is in `docs/` (not `drafts/`) and `status: review` or `approved`.
- Confluence MCP server is configured and reachable. **Status: planned** — if the MCP is
  not yet connected, stop and tell the operator what is needed (base URL, space key, token)
  instead of improvising another transport.

## Procedure

1. Confirm with the operator: which document, which **space**, which **parent page**,
   create-new vs update-existing.
2. Convert Markdown → Confluence storage format. Mermaid: use the Mermaid/diagram macro if
   available in the space; otherwise embed a rendered image and attach the `.mmd` source.
3. Preserve the template's section order and headings.
4. Create/update the page via the Confluence MCP.
5. Record the result in the document's changelog (page URL, date), set `status: approved`,
   and write the returned page id/url/version back into `publish/publish-map.yaml`.

## Corporate-standard note

Each KB may enforce its own corporate standard (labels, page tree, templates, approvals).
Ask for and follow the target space's conventions; do not assume the portfolio template
overrides them — map our sections onto their required structure.
