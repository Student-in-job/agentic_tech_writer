---
description: Start a document from the template library, or add/update a template (template-library)
argument-hint: <doc kind> [backend: confluence|gdocs|md]
---

Use the **template-library** skill for: `$ARGUMENTS`

If starting a document: ask (or infer) the document kind and storage backend (default
Confluence), pick the matching template from `templates/README.md`, resolve the document
unit (page/file; single vs multi), copy it into `drafts/`, and fill it — pulling technical
content from `code-recon` and diagrams from `diagram-builder` as needed. Draft only; never
publish.

If maintaining the library: add/update a template from `_meta-template.md`, grounding any
C4/TOGAF/BIAN structure via web/context7, and register it in the catalog.
