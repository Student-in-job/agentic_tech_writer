---
description: Export a service's or project's approved docs to Google Docs, PDF, Notion or Confluence
argument-hint: "<type: gdocs|pdf|notion|confluence> <source: service or project> <destination>"
---

Export documentation: `$ARGUMENTS`

Arguments — `<type> <source name> <destination>`:

- **type** — `gdocs` (Google Docs), `pdf`, `notion`, `confluence`. Accept the spoken forms too
  ("Google Docs", "PDF", "Notion", "Confluence").
- **source name** — a service or a project from `docs/registry.yaml`. A project exports every
  member service that has approved documents (services with only a card are skipped).
- **destination** — where to put it: a Google Drive folder (`gdocs`), a local directory (`pdf`),
  a parent page (`notion`), a space / parent page (`confluence`).

This is an **operator-initiated** export (AGENTS.md §4 — No Auto-Publish). The command itself is
the "go" for the named source and destination; anything beyond that (another destination, sharing,
deleting files that are already there) needs a separate confirmation. Markdown in `docs/` stays the
source of truth — never edit the exported copies.

## What gets produced

```
<destination>/docs/<project>/services/<service>/
    <service> — оглавление.<ext>     table of contents with links to every file
    <Type>/<document>.<ext>          one folder per document type: API, Architecture, Requirements, …
    diagrams/<diagram>.drawio|.svg   every Mermaid diagram, as draw.io and SVG
```

Every document carries its **version** (metadata table, footer, file properties). Documents
without a number show the schema snapshot or the revision date. Mermaid diagrams are rendered
to SVG and embedded (as PNG in DOCX — Google Docs cannot display SVG; as vector in PDF).

## Procedure

1. **Check the transport first.** If it is missing, stop and say exactly what is missing — do
   not switch to another transport.

   | type | needs |
   |------|-------|
   | `gdocs` | Google Drive for desktop (the Drive mount) **and** the Google Drive MCP connector |
   | `pdf` | Chrome or Edge installed (headless printing) |
   | `notion` | Notion MCP connector |
   | `confluence` | `confluence-publish` skill prerequisites (base URL, space, token in the environment) |

   Diagram rendering needs Chrome/Edge and network access to the Mermaid CDN for every type.

2. **Dry-run** and show the plan:
   `python scripts/docs_export.py <type> <source> "<destination>" --dry-run`

3. **Export** — run the same command without `--dry-run`. The script builds everything in
   `out/export/<type>/<source>/` and writes `manifest.json` there.

4. **Type-specific transport**

   - **gdocs** — the script copies the tree into the synced Drive folder. Links need Drive URLs:
     1. wait for the sync, then list the exported files with the Drive MCP (`search_files`,
        `parentId = '<folder id>'`, folder by folder);
     2. write a JSON file in the scratchpad: `{"docs/<project>/…/<file>": {"id": "…", "url": "…"}}`
        — keys are the `path` values from `manifest.json`;
     3. re-run with `--links <file>` — the table of contents and cross-references between
        documents get real links. Overwriting keeps the Drive file ids, so links stay valid.
   - **pdf** — the script writes the tree to the destination directory; nothing else to do.
   - **notion** — for each document in `manifest.json` create or update a page under the
     destination parent with the Notion MCP, using the normalised Markdown from the bundle;
     upload diagrams as images. Consult `publish/publish-map.yaml` for create-vs-update.
   - **confluence** — hand each bundle document to the `confluence-publish` skill.

5. **Record & report** — ids / urls go to `publish/publish-map.yaml` (the script does this for
   `gdocs --links`; for Notion / Confluence write them after the MCP calls). Report the root
   link, what was created vs. updated, and anything skipped.
