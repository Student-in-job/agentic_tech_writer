---
description: Publish a finished document to Confluence (manual, operator-initiated)
argument-hint: <document in docs/>
---

Use the **confluence-publish** skill to publish: `$ARGUMENTS`

This is a manual, operator-initiated delivery (AGENTS.md §4 — No Auto-Publish). Before
publishing, confirm with me: the exact document, the target space, the parent page, and
create-new vs update-existing. The document must live in `docs/` and be review-ready. If
the Confluence MCP is not connected, stop and tell me what is needed (base URL, space key,
token) instead of using another transport.
